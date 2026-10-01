
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
from aiohttp import web
from plugins import web_server

from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
from config import LOGGER, PORT, OWNER_ID, SHORT_URL, SHORT_API, SHORT_TUT, LOG_CHANNEL
from helper import MongoDB

version = "v1.0.0"


class Bot(Client):
    def __init__(self, session, workers, db, fsub, token, admins, messages, auto_del, db_uri, db_name, api_id, api_hash, protect, disable_btn):
        super().__init__(
            name=session,
            api_hash=api_hash,
            api_id=api_id,
            plugins={
                "root": "plugins"
            },
            workers=workers,
            bot_token=token
        )
        self.LOGGER = LOGGER
        self.name = session
        self.db = db
        self.fsub = fsub
        self.owner = OWNER_ID
        self.fsub_dict = {}
        self.forced_fsub_ids = set()   # channel ids that come from the global Forced FSUB list
        self._fsub_synced = False
        self._fsub_task = None
        self.admins = admins + [OWNER_ID] if OWNER_ID not in admins else admins
        self.messages = messages
        self.auto_del = auto_del
        self.protect = protect
        self.req_fsub = {}
        self.disable_btn = disable_btn
        self.reply_text = messages.get('REPLY', 'Do not send any useless message in the bot.')
        self.mongodb = MongoDB(db_uri, db_name)
        self.req_channels = []
        self.db_channels = {}
        self.primary_db_channel = db
        self.file_prefix = ""
        self.file_caption_template = ""
        self.file_buttons = []
        self.log_channel = LOG_CHANNEL
        self.caption_blacklist = []
    
    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        self.bot_id = usr_bot_me.username  # Unique namespace for this bot in shared DB

        # Create TTL indexes once per DB (safe/no-op if they already exist) so
        # abandoned shortner tokens auto-expire instead of growing forever.
        try:
            await self.mongodb.ensure_indexes()
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Error ensuring DB indexes: {e}")

        # FSUBS in config.py is intentionally ignored.
        # Force-sub channels are loaded only from the database (set via bot settings).

        # Load fsub channels: this bot's own list + the global Forced FSUB list
        # (shared by every bot on this DB), minus globally banned channels.
        try:
            await self.sync_fsub()
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Error loading fsub channels: {e}")
        # Keep picking up Forced FSUB adds/bans made from any linked bot
        self._fsub_task = asyncio.create_task(self._fsub_sync_loop())

        # Load DB channels from database
        try:
            db_channels_data = await self.mongodb.get_db_channels(self.bot_id)
            self.db_channels = {}
            self.primary_db_channel = self.db

            for channel_id_str, channel_data in db_channels_data.items():
                channel_id = int(channel_id_str)
                try:
                    chat = await self.get_chat(channel_id)
                    channel_data['name'] = chat.title
                    self.db_channels[channel_id_str] = channel_data
                    if channel_data.get('is_primary', False):
                        self.primary_db_channel = channel_id
                        self.db = channel_id
                except Exception as e:
                    self.LOGGER(__name__, self.name).warning(f"Could not load DB channel {channel_id}: {e}")
                    await self.mongodb.remove_db_channel(channel_id, self.bot_id)
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Error loading DB channels: {e}")

        # Load shortner settings from database (multi-shortner support)
        try:
            shortner_settings = await self.mongodb.get_shortner_settings(self.bot_id)
            shorteners = shortner_settings.get('shorteners', {})
            active = shortner_settings.get('active')

            # Migrate legacy single-shortner config into the new multi-shortner format
            if not shorteners:
                legacy_url = shortner_settings.get('short_url', SHORT_URL)
                legacy_api = shortner_settings.get('short_api', SHORT_API)
                if legacy_url and legacy_api:
                    shorteners = {
                        'default': {
                            'url': legacy_url,
                            'api': legacy_api,
                            'tutorial_link': shortner_settings.get('tutorial_link', SHORT_TUT)
                        }
                    }
                    active = 'default'
                    await self.mongodb.update_shortner_setting('shorteners', shorteners, self.bot_id)
                    await self.mongodb.update_shortner_setting('active', active, self.bot_id)

            self.shorteners = shorteners
            self.active_shortener = active if active in shorteners else (next(iter(shorteners), None))
            self.shortner_enabled = shortner_settings.get('enabled', True)

            # Mirror attrs for backward compatibility with plugins that read short_url/short_api/tutorial_link directly
            active_cfg = shorteners.get(self.active_shortener, {}) if self.active_shortener else {}
            self.short_url = active_cfg.get('url', SHORT_URL)
            self.short_api = active_cfg.get('api', SHORT_API)
            self.tutorial_link = active_cfg.get('tutorial_link', SHORT_TUT)
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Error loading shortner settings: {e}")
            self.shorteners = {}
            self.active_shortener = None
            self.shortner_enabled = True
            self.short_url = SHORT_URL
            self.short_api = SHORT_API
            self.tutorial_link = SHORT_TUT

        # Load auto-mode shortner settings (separate ordered list, cycles per-user)
        try:
            auto_settings = await self.mongodb.get_auto_shortner_settings(self.bot_id)
            self.auto_shorteners = auto_settings.get('shorteners', [])
            self.auto_shortener_enabled = auto_settings.get('enabled', False)
            # Rotation mode — position #1 of the auto list cycles between 2 links on a timer
            self.rotation_enabled = auto_settings.get('rotation_enabled', False)
            self.rotation_links = auto_settings.get('rotation_links', [])
            self.rotation_timer_hours = auto_settings.get('rotation_timer_hours', 2)
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Error loading auto shortner settings: {e}")
            self.auto_shorteners = []
            self.auto_shortener_enabled = False
            self.rotation_enabled = False
            self.rotation_links = []
            self.rotation_timer_hours = 2

        # Load file prefix, caption template and custom buttons from database
        try:
            self.file_prefix = await self.mongodb.get_bot_setting('file_prefix', '', self.bot_id)
            self.file_caption_template = await self.mongodb.get_bot_setting('file_caption_template', '', self.bot_id)
            self.file_buttons = await self.mongodb.get_bot_setting('file_buttons', [], self.bot_id)
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Error loading file settings: {e}")
            self.file_prefix = ""
            self.file_caption_template = ""
            self.file_buttons = []

        # Load messages settings from database (overrides config on restart)
        # Each bot uses its own bot_id namespace so multiple bots share same DB safely
        try:
            db_messages = await self.mongodb.get_messages_settings(self.bot_id)
            if db_messages:
                self.messages.update(db_messages)
                self.reply_text = self.messages.get('REPLY', self.reply_text)
            self.LOGGER(__name__, self.name).info(f"Messages settings loaded from DB for bot: {self.bot_id}")
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Error loading messages settings: {e}")
        
        try:
            db_channel = await self.get_chat(self.db)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Testing Message by @ProYato")
            await test.delete()
            
            # Log DB channels info
            self.LOGGER(__name__, self.name).info(f"Primary DB Channel: {self.primary_db_channel}")
            self.LOGGER(__name__, self.name).info(f"Total DB Channels: {len(self.db_channels)}")
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(e)
            self.LOGGER(__name__, self.name).warning(f"Make Sure bot is Admin in DB Channel, and Double check the database channel Value, Current Value {self.db}")
            self.LOGGER(__name__, self.name).info("\nBot Stopped. Join https://t.me/animes_cruise for support")
            sys.exit()
        try:
            self.caption_blacklist = await self.mongodb.get_bot_setting('caption_blacklist', [], self.bot_id)
            self.LOGGER(__name__, self.name).info(f"Blacklist loaded: {self.caption_blacklist}")
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Error loading blacklist: {e}")
            self.caption_blacklist = []

        self.LOGGER(__name__, self.name).info("Bot Started!!")
        
        # Send restart msge to owner
        try:
            restart_message = "<b>›› ʜᴇʏ sᴇɴᴘᴀɪ!!\n ɪ'ᴍ ᴀʟɪᴠᴇ ɴᴏᴡ 🍃...</b>"
            await self.send_message(chat_id=self.owner, text=restart_message)
            self.LOGGER(__name__, self.name).info(f"Restart notification sent to owner: {self.owner}")
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Failed to send restart notification to owner: {e}")
        
        self.username = usr_bot_me.username
    async def sync_fsub(self):
        """Rebuild fsub_dict = own channels + global forced channels - banned channels.
        Safe to call repeatedly; never deletes anything from the DB."""
        banned = {int(x) for x in await self.mongodb.get_banned_fsub()}
        own = await self.mongodb.get_fsub_channels(self.bot_id)
        forced = await self.mongodb.get_forced_fsub()
        old = self.fsub_dict
        new, forced_ids = {}, set()

        for source, is_forced in ((own, False), (forced, True)):  # forced overrides own
            for cid_str, data in source.items():
                try:
                    cid = int(cid_str)
                except (TypeError, ValueError):
                    continue
                if cid in banned or not isinstance(data, list) or len(data) != 4:
                    continue
                data = list(data)
                if cid in old:
                    data[0] = old[cid][0]          # reuse cached name
                else:
                    try:
                        data[0] = (await self.get_chat(cid)).title
                    except Exception as e:
                        self.LOGGER(__name__, self.name).warning(f"Could not load fsub channel {cid}: {e}")
                        continue
                if data[3] == 0 and not data[1]:
                    try:
                        link = await self.create_chat_invite_link(cid, creates_join_request=data[2])
                        data[1] = link.invite_link
                    except Exception as e:
                        self.LOGGER(__name__, self.name).warning(f"Could not create invite link for {cid}: {e}")
                new[cid] = data
                if is_forced:
                    forced_ids.add(cid)

        self.fsub_dict = new                      # swap, don't mutate (handlers may be iterating)
        self.forced_fsub_ids = forced_ids
        req = [cid for cid, d in new.items() if d[2]]
        if req != self.req_channels or not self._fsub_synced:
            self.req_channels = req
            try:
                await self.mongodb.set_channels(req)
            except Exception as e:
                self.LOGGER(__name__, self.name).warning(f"Could not save req channels: {e}")
        self._fsub_synced = True

    async def _fsub_sync_loop(self, interval: int = 30):
        while True:
            await asyncio.sleep(interval)
            try:
                await self.sync_fsub()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self.LOGGER(__name__, self.name).warning(f"fsub sync failed: {e}")

    async def stop(self, *args):
        if self._fsub_task:
            self._fsub_task.cancel()
        await super().stop()
        self.LOGGER(__name__, self.name).info("Bot stopped.")


async def web_app():
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    
