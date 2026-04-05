import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from helper.helper_func import str_to_b64

#===============================================================#

# Batch collector: gather files sent together, sort by message_id, then process in order
_pending_files = []
_collect_task = None

async def _process_pending_files(client: Client):
    global _collect_task, _pending_files
    await asyncio.sleep(0.5)
    files = sorted(_pending_files, key=lambda m: m.id)
    _pending_files = []
    _collect_task = None

    for message in files:
        # Skip plain text messages - only generate links for media
        if not (message.photo or message.video or message.document or message.audio or message.voice or message.animation or message.sticker or message.video_note):
            continue

        try:
            post_message = await message.copy(chat_id=client.db, disable_notification=True)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                post_message = await message.copy(chat_id=client.db, disable_notification=True)
            except Exception as err:
                await message.reply_text(f"Something went Wrong!\n\n**Error:** `{err}`")
                continue
        except Exception as e:
            await message.reply_text(f"Something went Wrong!\n\n**Error:** `{e}`")
            continue

        # Luffy-style: encode plain message ID with str_to_b64
        file_er_id = str(post_message.id)
        link = f"https://t.me/{client.username}?start=F2Botz_{str_to_b64(file_er_id)}"

        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')
        ]])

        await message.reply(
            f"<b>Your File Stored in my Database!</b>\n\n"
            f"Here is the Permanent Link of your file:\n<code>{link}</code>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=False
        )

        if not client.disable_btn:
            try:
                await post_message.edit_reply_markup(reply_markup)
            except Exception:
                pass

#===============================================================#

@Client.on_message(filters.private & ~filters.command(['start', 'shortner','users','broadcast','batch','genlink','stats', 'pbroadcast', 'db', 'adddb', 'add_db', 'removedb', 'rm_db',  'ban', 'unban', 'addpremium', 'delpremium', 'premiumusers', 'request', 'profile']))
async def channel_post(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply(client.reply_text)

    # Collect files sent in quick succession, then process them all at once
    global _collect_task, _pending_files
    _pending_files.append(message)
    if _collect_task is not None:
        _collect_task.cancel()
    loop = asyncio.get_event_loop()
    _collect_task = loop.create_task(_process_pending_files(client))

#===============================================================#

@Client.on_message(filters.channel & filters.incoming)
async def new_post(client: Client, message: Message):
    if message.chat.id != client.db:
        return
    if client.disable_btn:
        return

    # Luffy-style link for channel posts already stored in DB channel
    file_er_id = str(message.id)
    link = f"https://t.me/{client.username}?start=F2Botz_{str_to_b64(file_er_id)}"
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')
    ]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
