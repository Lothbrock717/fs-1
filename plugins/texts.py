from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

#===============================================================#

async def show_texts_menu(client, query):
    msg = f"""<blockquote>**Text Configuration:**</blockquote>
**Start Message:**
<pre>{client.messages.get('START', 'Empty')}</pre>
**Force Sub Message:**
<pre>{client.messages.get('FSUB', 'Empty')}</pre>
**About Message:**
<pre>{client.messages.get('ABOUT', 'Empty')}</pre>
**Reply Message:**
<pre>{client.reply_text}</pre>
    """
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ꜱᴛᴀʀᴛ ᴛᴇxᴛ', 'start_txt'), InlineKeyboardButton('ꜰꜱᴜʙ ᴛᴇxᴛ', 'fsub_txt')],
        [InlineKeyboardButton('ʀᴇᴘʟʏ ᴛᴇxᴛ', 'reply_txt'), InlineKeyboardButton('ᴀʙᴏᴜᴛ ᴛᴇxᴛ', 'about_txt')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^texts$"))
async def texts(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    await show_texts_menu(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^start_txt$"))
async def start_txt(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    ask_text = await client.ask(query.from_user.id, "Send new start text in the next 60 seconds, send `0` to cancel.\n\n__Supports both markdown and HTML formatting!__", filters=filters.text, timeout=60)
    try:
        text = ask_text.text
        if text == '0':
            return await ask_text.reply("__Start text has not changed!__")
        client.messages['START'] = text
        await show_texts_menu(client, query)
        return await ask_text.reply("__Start text has been changed!__")
    except Exception as e:
        return await ask_text.reply(f"**Error:** `{e}`")

#===============================================================#

@Client.on_callback_query(filters.regex("^fsub_txt$"))
async def force_txt(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    ask_text = await client.ask(query.from_user.id, "Send new force sub text in the next 60 seconds, send `0` to cancel.\n\n__Supports both markdown and HTML formatting!__", filters=filters.text, timeout=60)
    try:
        text = ask_text.text
        if text == '0':
            return await ask_text.reply("__Force Sub text has not changed!__")
        client.messages['FSUB'] = text
        await show_texts_menu(client, query)
        return await ask_text.reply("__Force Sub text has been changed!__")
    except Exception as e:
        return await ask_text.reply(f"**Error:** `{e}`")

#===============================================================#

@Client.on_callback_query(filters.regex("^about_txt$"))
async def about_txt(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    ask_text = await client.ask(query.from_user.id, "Send new about text in the next 60 seconds, send `0` to cancel.\n\n__Supports both markdown and HTML formatting!__", filters=filters.text, timeout=60)
    try:
        text = ask_text.text
        if text == '0':
            return await ask_text.reply("__About text has not changed!__")
        client.messages['ABOUT'] = text
        await show_texts_menu(client, query)
        return await ask_text.reply("__About text has been changed!__")
    except Exception as e:
        return await ask_text.reply(f"**Error:** `{e}`")

#===============================================================#

@Client.on_callback_query(filters.regex("^reply_txt$"))
async def reply_txt(client: Client, query: CallbackQuery):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    ask_text = await client.ask(query.from_user.id, "Send new reply text in the next 60 seconds, send `0` to cancel.", filters=filters.text, timeout=60)
    try:
        text = ask_text.text
        if text == '0':
            return await ask_text.reply("__Reply text has not changed!__")
        client.reply_text = text
        await show_texts_menu(client, query)
        return await ask_text.reply("__Reply text has been changed!__")
    except Exception as e:
        return await ask_text.reply(f"**Error:** `{e}`")
