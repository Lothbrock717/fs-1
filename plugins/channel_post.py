import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from helper.helper_func import encode

#===============================================================#

@Client.on_message(filters.private & ~filters.command([
    'start', 'shortner','users','broadcast','batch','genlink','stats',
    'pbroadcast', 'db', 'adddb', 'add_db', 'removedb', 'rm_db',
    'ban', 'unban', 'addpremium', 'delpremium', 'premiumusers',
    'request', 'profile'
]))
async def channel_post(client: Client, message: Message):

    # 🔐 Admin check (UNCHANGED)
    if message.from_user.id not in client.admins:
        return await message.reply(client.reply_text)

    reply_text = await message.reply_text("Please Wait...!", quote=True)

    try:
        # 🔥 SAVE FILE TO DB CHANNEL (LUFFY SYSTEM STYLE)
        post_message = await message.copy(
            chat_id=client.db,
            disable_notification=True
        )

    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(
            chat_id=client.db,
            disable_notification=True
        )

    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return

    # 🔥 KEEP ORIGINAL FS-1 LINK SYSTEM (IMPORTANT)
    converted_id = post_message.id * abs(client.db)
    string = f"get-{converted_id}"
    base64_string = await encode(string)

    link = f"https://t.me/{client.username}?start={base64_string}"

    # 🔘 BUTTON (UNCHANGED)
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )

    # 📩 SEND LINK (UNCHANGED)
    await reply_text.edit(
        f"<b>Here is your link</b>\n\n{link}",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    # 🔘 ADD BUTTON TO STORED MESSAGE (UNCHANGED)
    if not client.disable_btn:
        await post_message.edit_reply_markup(reply_markup)

#===============================================================#

@Client.on_message(filters.channel & filters.incoming)
async def new_post(client: Client, message: Message):

    # 🔒 ONLY DB CHANNEL
    if message.chat.id != client.db:
        return

    if client.disable_btn:
        return

    # 🔥 SAME LINK GENERATION (UNCHANGED)
    converted_id = message.id * abs(client.db)
    string = f"get-{converted_id}"
    base64_string = await encode(string)

    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )

    try:
        await message.edit_reply_markup(reply_markup)

    except Exception as e:
        print(e)
        pass
