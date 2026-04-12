from helper.helper_func import *
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import humanize
from config import MSG_EFFECT, OWNER_ID
from plugins.shortner import get_short
from helper.helper_func import force_sub, batch_auto_del_notification
from helper.helper_func import str_to_b64, b64_to_str
import asyncio
import re

#===============================================================#

def clean_caption(text: str) -> str:
    """Strip links, HTML tags, promotional lines and leftover dashes from caption."""
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove http/https links
    text = re.sub(r'https?://\S+', '', text)
    # Remove t.me links
    text = re.sub(r't\.me/\S+', '', text)
    # Remove @usernames
    text = re.sub(r'@\w+', '', text)
    # Remove FOR MORE lines (including unicode bold/italic variants) and everything after
    text = re.sub(r'(?i)\bfor more\b.*', '', text, flags=re.DOTALL)
    # Remove unicode styled "FOR MORE" (𝙁𝙊𝙍 𝙈𝙊𝙍𝙀) - match by unicode range
    text = re.sub(r'[\U0001D400-\U0001D7FF\U0001D600-\U0001D9FF]+\s*[:\-]?.*', '', text, flags=re.DOTALL)
    # Remove ~ lines (channel promotions like ~ Yagami Universe)
    text = re.sub(r'~.*', '', text, flags=re.DOTALL)
    # Remove "• File name :" prefix
    text = re.sub(r'(?i)•?\s*file\s*name\s*[:\-]?\s*', '', text)
    # Remove Join lines
    text = re.sub(r'(?i)join.*', '', text)
    # Remove leading/trailing dashes and separators
    text = re.sub(r'^[\s\-–—|•:]+', '', text)
    text = re.sub(r'[\s\-–—|]+$', '', text)
    # Collapse multiple spaces/newlines
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def build_caption(client, raw_caption: str) -> str:
    """Build final caption using custom template or prefix, after stripping original links."""
    cleaned = clean_caption(raw_caption)
    template = getattr(client, 'file_caption_template', '')
    if template:
        return template.replace('{original_caption}', cleaned).replace('{filename}', cleaned)
    prefix = getattr(client, 'file_prefix', '')
    if prefix and cleaned:
        return f"{prefix} - {cleaned}"
    elif prefix:
        return prefix
    return cleaned

def build_file_buttons(client):
    """Build inline buttons from client.file_buttons list."""
    custom_buttons = getattr(client, 'file_buttons', [])
    if not custom_buttons:
        return None
    rows = []
    for row in custom_buttons:
        btn_row = []
        for btn in row:
            try:
                btn_row.append(InlineKeyboardButton(btn['text'], url=btn['url']))
            except Exception:
                pass
        if btn_row:
            rows.append(btn_row)
    return InlineKeyboardMarkup(rows) if rows else None

#===============================================================#

@Client.on_message(filters.command('start') & filters.private)
@force_sub
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # 1. Add user if not present
    present = await client.mongodb.present_user(user_id)
    if not present:
        try:
            await client.mongodb.add_user(user_id)
        except Exception as e:
            client.LOGGER(__name__, client.name).warning(f"Error adding a user:\n{e}")
        # Send new user log to LOG_CHANNEL (safe — won't crash if bot not in channel)
        try:
            if getattr(client, 'log_channel', None):
                user = message.from_user
                name = user.first_name or ""
                if user.last_name:
                    name += f" {user.last_name}"
                mention = f"<a href='tg://user?id={user_id}'>{name}</a>"
                log_text = (
                    f"#NEW_USER:\n\n"
                    f"New User {mention} started @{client.username} !!"
                )
                await client.send_message(chat_id=client.log_channel, text=log_text)
        except Exception as e:
            client.LOGGER(__name__, client.name).warning(f"Failed to send new user log: {e}")

    # 2. Check if banned
    is_banned = await client.mongodb.is_banned(user_id)
    if is_banned:
        return await message.reply("**You have been banned from using this bot!**")

    text = message.text or ""
    # Extract payload — handle /start, /start@BotUsername, /start payload formats
    payload_parts = text.strip().split(None, 1)
    raw_payload = payload_parts[1].strip() if len(payload_parts) > 1 else ""
    # Strip @BotUsername from command if present (e.g. /start@MyBot payload)
    if raw_payload.startswith("@"):
        raw_payload = raw_payload.split(None, 1)[1].strip() if " " in raw_payload else ""

    if raw_payload:
        original_payload = raw_payload

        # 3. Check premium status
        is_user_pro = await client.mongodb.is_pro(user_id)

        # 4. Check if shortner is enabled
        shortner_enabled = getattr(client, 'shortner_enabled', False)
        short_url = getattr(client, 'short_url', '')
        short_api = getattr(client, 'short_api', '')
        # Disable shortner if url or api not configured
        if not short_url or not short_api:
            shortner_enabled = False

        # ── Luffy-style shortner: wrap non-premium users with short link ──────
        # Short links use prefix "yu3elk" so we know to skip them on second hit
        is_short_link = original_payload.startswith("yu3elk")

        if not is_user_pro and user_id != OWNER_ID and not is_short_link and shortner_enabled:
            try:
                short_link = get_short(
                    f"https://t.me/{client.username}?start=yu3elk{original_payload}7",
                    client
                )
            except Exception as e:
                client.LOGGER(__name__, client.name).warning(f"Shortener failed: {e}")
                return await message.reply("Couldn't generate short link.")

            short_photo = client.messages.get("SHORT_PIC", "")
            short_caption = client.messages.get("SHORT_MSG", "")
            tutorial_link = getattr(client, 'tutorial_link', "https://t.me/How_to_Download_7x/26")

            await client.send_photo(
                chat_id=message.chat.id,
                photo=short_photo,
                caption=short_caption,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("• ᴏᴘᴇɴ ʟɪɴᴋ", url=short_link),
                        InlineKeyboardButton("ᴛᴜᴛᴏʀɪᴀʟ •", url=tutorial_link)
                    ],
                    [
                        InlineKeyboardButton(" • ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •", url="https://t.me/+V7zUi7O_DkEyNGZl")
                    ]
                ])
            )
            return

        # Strip the short-link prefix if present before decoding
        payload = original_payload
        if is_short_link:
            payload = payload[6:-1]  # strip "yu3elk" prefix and trailing "7"

        # ── Decode Luffy-style links ──────────────────────────────────────────

        # batch link: start=batch-<b64 of space-separated IDs>
        if payload.startswith("batch-"):
            _, files_id = payload.split("-", 1)
            try:
                decoded = b64_to_str(files_id)
                if " " in decoded:
                    msg_ids = [int(x) for x in decoded.split()]
                elif "-" in decoded:
                    parts = decoded.split("-")
                    start_id, end_id = int(parts[0]), int(parts[1])
                    msg_ids = list(range(start_id, end_id + 1))
                else:
                    msg_ids = [int(decoded)]
            except Exception as e:
                client.LOGGER(__name__, client.name).warning(f"Batch decode error: {e}")
                return await message.reply("⚠️ Invalid or expired batch link.")

            temp_msg = await message.reply("Wait A Sec..")
            yugen_msgs = []
            for msg_id in msg_ids:
                try:
                    db_msg = await client.get_messages(chat_id=client.db, message_ids=msg_id)
                    if db_msg and not db_msg.empty:
                        _raw_caption = "" if not db_msg.caption else db_msg.caption.html
                        caption = build_caption(client, _raw_caption)
                        reply_markup = build_file_buttons(client) or (db_msg.reply_markup if not client.disable_btn else None)
                        copied = await db_msg.copy(
                            chat_id=message.from_user.id,
                            caption=caption,
                            reply_markup=reply_markup,
                            protect_content=client.protect
                        )
                        yugen_msgs.append(copied)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as e:
                    client.LOGGER(__name__, client.name).warning(f"Failed to send batch file {msg_id}: {e}")

            await temp_msg.delete()
            if not yugen_msgs:
                return await message.reply(f"Couldn't find the files in the database.\nDB: `{client.db}`")

        # F2Botz_ single-file link (admin-saved private files)
        elif payload.startswith("F2Botz_"):
            encoded = payload[7:]
            try:
                file_id = int(b64_to_str(encoded))
            except Exception as e:
                client.LOGGER(__name__, client.name).warning(f"F2Botz decode error: {e}")
                return await message.reply("⚠️ Invalid or expired link.")

            temp_msg = await message.reply("Wait A Sec..")
            try:
                db_msg = await client.get_messages(chat_id=client.db, message_ids=file_id)
                if db_msg and not db_msg.empty:
                    # Handle the case where the DB message is a text listing multiple IDs
                    if db_msg.text:
                        message_ids = db_msg.text.split()
                        await temp_msg.edit_text(f"**Total Files:** `{len(message_ids)}`")
                        yugen_msgs = []
                        for mid in message_ids:
                            try:
                                sub_msg = await client.get_messages(chat_id=client.db, message_ids=int(mid))
                                _raw_caption = "" if not sub_msg.caption else sub_msg.caption.html
                                caption = build_caption(client, _raw_caption)
                                reply_markup = build_file_buttons(client) or (sub_msg.reply_markup if not client.disable_btn else None)
                                copied = await sub_msg.copy(
                                    chat_id=message.from_user.id,
                                    caption=caption,
                                    reply_markup=reply_markup,
                                    protect_content=client.protect
                                )
                                yugen_msgs.append(copied)
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                            except Exception as e:
                                client.LOGGER(__name__, client.name).warning(f"Failed to send file {mid}: {e}")
                    else:
                        _raw_caption = "" if not db_msg.caption else db_msg.caption.html
                        caption = build_caption(client, _raw_caption)
                        reply_markup = build_file_buttons(client) or (db_msg.reply_markup if not client.disable_btn else None)
                        copied_msg = await db_msg.copy(
                            chat_id=message.from_user.id,
                            caption=caption,
                            reply_markup=reply_markup,
                            protect_content=client.protect
                        )
                        yugen_msgs = [copied_msg]
                        await temp_msg.delete()
                else:
                    await temp_msg.delete()
                    return await message.reply("Couldn't find the file in the database.")
            except Exception as e:
                await temp_msg.edit_text(f"Something went wrong!\n`{e}`")
                client.LOGGER(__name__, client.name).warning(f"Error getting file {file_id}: {e}")
                return

        else:
            return await message.reply("⚠️ Invalid or expired link.")

        # 8. Auto delete timer
        if yugen_msgs and client.auto_del > 0:
            asyncio.create_task(batch_auto_del_notification(
                bot_username=client.username,
                messages=yugen_msgs,
                delay_time=client.auto_del,
                transfer_link=original_payload,
                chat_id=message.from_user.id,
                client=client
            ))
        return

    # 9. Normal start message
    else:
        buttons = [[InlineKeyboardButton("Help", callback_data="about"), InlineKeyboardButton("Close", callback_data='close')]]
        if user_id in client.admins:
            buttons.insert(0, [InlineKeyboardButton("⛩️ ꜱᴇᴛᴛɪɴɢꜱ ⛩️", callback_data="settings")])

        photo = client.messages.get("START_PHOTO", "")
        start_caption = client.messages.get('START', 'Welcome, {mention}').format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        )

        if photo:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=start_caption,
                message_effect_id=MSG_EFFECT,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await client.send_message(
                chat_id=message.chat.id,
                text=start_caption,
                message_effect_id=MSG_EFFECT,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        return

#===============================================================#

@Client.on_message(filters.command('request') & filters.private)
async def request_command(client: Client, message: Message):
    user_id = message.from_user.id
    is_admin = user_id in client.admins  # ✅ Fix this line
    is_user_premium = await client.mongodb.is_pro(user_id)

    if is_admin or user_id == OWNER_ID:
        await message.reply_text("🔹 **You are my sensei!**\nThis command is only for users.")
        return

    if not is_user_premium: 
        BUTTON_URL = "https://t.me/+r-ez-AY7i3djNmM1"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Upgrade to Premium", url=BUTTON_URL)]
        ])
        await message.reply(
            "❌ **You are not a premium user.**\nUpgrade to premium to access this feature.",
            reply_markup=reply_markup
        )
        return

    if len(message.command) < 2:
        await message.reply("⚠️ **Send me your request in this format:**\n`/request Your_Request_Here`")
        return

    requested = " ".join(message.command[1:])

    owner_message = (
        f"📩 **New Request from {message.from_user.mention}**\n\n"
        f"🆔 User ID: `{user_id}`\n"
        f"📝 Request: `{requested}`"
    )

    await client.send_message(OWNER_ID, owner_message)
    await message.reply("✅ **Thanks for your request!**\nYour request will be reviewed soon. Please wait.")

#===============================================================#

@Client.on_message(filters.command('profile') & filters.private)
async def my_plan(client: Client, message: Message):
    user_id = message.from_user.id
    is_admin = user_id in client.admins  # ✅ Fix here

    if is_admin or user_id == OWNER_ID:
        await message.reply_text("🔹 You're my sensei! This command is only for users.")
        return
    
    is_user_premium = await client.mongodb.is_pro(user_id)

    if is_user_premium:
        await message.reply_text(
            "**👤 Profile Information:**\n\n"
            "🔸 Ads: Disabled\n"
            "🔸 Plan: Premium\n"
            "🔸 Request: Enabled\n\n"
            "🌟 You're a Premium User!"
        )
    else:
        await message.reply_text(
            "**👤 Profile Information:**\n\n"
            "🔸 Ads: Enabled\n"
            "🔸 Plan: Free\n"
            "🔸 Request: Disabled\n\n"
            "🔓 Unlock Premium to get more benefits\n"
            "Contact: @F2_Adminn"
        )
