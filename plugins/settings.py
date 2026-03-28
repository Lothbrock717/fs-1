from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.pyromod import ListenerTimeout
from config import OWNER_ID

#===============================================================#

@Client.on_callback_query(filters.regex("^settings$"))
async def settings(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    total_fsub = len(client.fsub_dict)
    request_enabled = sum(1 for data in client.fsub_dict.values() if data[2])
    timer_enabled = sum(1 for data in client.fsub_dict.values() if data[3] > 0)
    total_db_channels = len(getattr(client, 'db_channels', {}))
    primary_db = getattr(client, 'primary_db_channel', client.db)
    _start_prev = (client.messages.get('START', 'ᴇᴍᴘᴛʏ') or 'ᴇᴍᴘᴛʏ')[:200]
    _fsub_prev = (client.messages.get('FSUB', 'ᴇᴍᴘᴛʏ') or 'ᴇᴍᴘᴛʏ')[:200]
    _about_prev = (client.messages.get('ABOUT', 'ᴇᴍᴘᴛʏ') or 'ᴇᴍᴘᴛʏ')[:200]
    _reply_prev = (client.reply_text or '')[:200]
    msg = f"""<blockquote>✦ sᴇᴛᴛɪɴɢs ᴏғ @{client.username}</blockquote>
›› **ꜰꜱᴜʙ ᴄʜᴀɴɴᴇʟs:** `{total_fsub}` (ʀᴇǫᴜᴇsᴛ: {request_enabled}, ᴛɪᴍᴇʀ: {timer_enabled})
›› **ᴅʙ ᴄʜᴀɴɴᴇʟs:** `{total_db_channels}` (ᴘʀɪᴍᴀʀʏ: `{primary_db}`)
›› **ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ:** `{client.auto_del}`
›› **ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ:** `{"✓ ᴛʀᴜᴇ" if client.protect else "✗ ꜰᴀʟsᴇ"}`
›› **ᴅɪsᴀʙʟᴇ ʙᴜᴛᴛᴏɴ:** `{"✓ ᴛʀᴜᴇ" if client.disable_btn else "✗ ꜰᴀʟsᴇ"}`
›› **ꜰɪʟᴇ ᴘʀᴇꜰɪx:** `{getattr(client, 'file_prefix', '') or 'ɴᴏᴛ sᴇᴛ'}`
›› **ʀᴇᴘʟʏ ᴛᴇxᴛ:** `{client.reply_text if client.reply_text else 'ɴᴏɴᴇ'}`
›› **ᴀᴅᴍɪɴs:** `{len(client.admins)}`
›› **sʜᴏʀᴛɴᴇʀ ᴜʀʟ:** `{getattr(client, 'short_url', 'ɴᴏᴛ sᴇᴛ')}`
›› **ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ:** `{getattr(client, 'tutorial_link', 'ɴᴏᴛ sᴇᴛ')}`
›› **sᴛᴀʀᴛ ᴍᴇssᴀɢᴇ:**
<pre>{_start_prev}</pre>
›› **sᴛᴀʀᴛ ɪᴍᴀɢᴇ:** `{bool(client.messages.get('START_PHOTO', ''))}`
›› **ꜰᴏʀᴄᴇ sᴜʙ ᴍᴇssᴀɢᴇ:**
<pre>{_fsub_prev}</pre>
›› **ꜰᴏʀᴄᴇ sᴜʙ ɪᴍᴀɢᴇ:** `{bool(client.messages.get('FSUB_PHOTO', ''))}`
›› **ᴀʙᴏᴜᴛ ᴍᴇssᴀɢᴇ:**
<pre>{_about_prev}</pre>
›› **ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ:**
<pre>{_reply_prev}</pre>
    """
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ꜰꜱᴜʙ ᴄʜᴀɴɴᴇʟꜱ', 'fsub'), InlineKeyboardButton('ᴅʙ ᴄʜᴀɴɴᴇʟꜱ', 'db_channels')],
        [InlineKeyboardButton('ᴀᴅᴍɪɴꜱ', 'admins'), InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ', 'auto_del')],
        [InlineKeyboardButton('ꜰɪʟᴇ ᴄᴀᴘᴛɪᴏɴ', 'file_prefix'), InlineKeyboardButton('ʜᴏᴍᴇ', 'home')],
        [InlineKeyboardButton('›› ɴᴇxᴛ', 'settings_page_2')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^settings_page_2$"))
async def settings_page_2(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    total_fsub = len(client.fsub_dict)
    request_enabled = sum(1 for data in client.fsub_dict.values() if data[2])
    timer_enabled = sum(1 for data in client.fsub_dict.values() if data[3] > 0)
    total_db_channels = len(getattr(client, 'db_channels', {}))
    primary_db = getattr(client, 'primary_db_channel', client.db)
    _start_prev = (client.messages.get('START', 'ᴇᴍᴘᴛʏ') or 'ᴇᴍᴘᴛʏ')[:200]
    _fsub_prev = (client.messages.get('FSUB', 'ᴇᴍᴘᴛʏ') or 'ᴇᴍᴘᴛʏ')[:200]
    _about_prev = (client.messages.get('ABOUT', 'ᴇᴍᴘᴛʏ') or 'ᴇᴍᴘᴛʏ')[:200]
    _reply_prev = (client.reply_text or '')[:200]
    msg = f"""<blockquote>✦ sᴇᴛᴛɪɴɢs ᴏғ @{client.username}</blockquote>
›› **ꜰsᴜʙ ᴄʜᴀɴɴᴇʟs:** `{total_fsub}` (ʀᴇǫᴜᴇsᴛ: {request_enabled}, ᴛɪᴍᴇʀ: {timer_enabled})
›› **ᴅʙ ᴄʜᴀɴɴᴇʟs:** `{total_db_channels}` (ᴘʀɪᴍᴀʀʏ: `{primary_db}`)
›› **ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ:** `{client.auto_del}`
›› **ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ:** `{"✓ ᴛʀᴜᴇ" if client.protect else "✗ ꜰᴀʟsᴇ"}`
›› **ᴅɪsᴀʙʟᴇ ʙᴜᴛᴛᴏɴ:** `{"✓ ᴛʀᴜᴇ" if client.disable_btn else "✗ ꜰᴀʟsᴇ"}`
›› **ꜰɪʟᴇ ᴘʀᴇꜰɪx:** `{getattr(client, 'file_prefix', '') or 'ɴᴏᴛ sᴇᴛ'}`
›› **ʀᴇᴘʟʏ ᴛᴇxᴛ:** `{client.reply_text if client.reply_text else 'ɴᴏɴᴇ'}`
›› **ᴀᴅᴍɪɴs:** `{len(client.admins)}`
›› **sʜᴏʀᴛɴᴇʀ ᴜʀʟ:** `{getattr(client, 'short_url', 'ɴᴏᴛ sᴇᴛ')}`
›› **ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ:** `{getattr(client, 'tutorial_link', 'ɴᴏᴛ sᴇᴛ')}`
›› **sᴛᴀʀᴛ ᴍᴇssᴀɢᴇ:**
<pre>{_start_prev}</pre>
›› **sᴛᴀʀᴛ ɪᴍᴀɢᴇ:** `{bool(client.messages.get('START_PHOTO', ''))}`
›› **ꜰᴏʀᴄᴇ sᴜʙ ᴍᴇssᴀɢᴇ:**
<pre>{_fsub_prev}</pre>
›› **ꜰᴏʀᴄᴇ sᴜʙ ɪᴍᴀɢᴇ:** `{bool(client.messages.get('FSUB_PHOTO', ''))}`
›› **ᴀʙᴏᴜᴛ ᴍᴇssᴀɢᴇ:**
<pre>{_about_prev}</pre>
›› **ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ:**
<pre>{_reply_prev}</pre>
    """
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ', 'protect'), InlineKeyboardButton('ᴘʜᴏᴛᴏs', 'photos')],
        [InlineKeyboardButton('ᴛᴇxᴛs', 'texts'), InlineKeyboardButton('sʜᴏʀᴛɴᴇʀ', 'shortner')],
        [InlineKeyboardButton('‹ ᴘʀᴇᴠ', 'settings'), InlineKeyboardButton('ʜᴏᴍᴇ', 'home')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^fsub$"))
async def fsub(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    if client.fsub_dict:
        channel_list = []
        for channel_id, channel_data in client.fsub_dict.items():
            channel_name = channel_data[0] if channel_data and len(channel_data) > 0 else "Unknown"
            request_status = "✓ ʀᴇѦᴜᴇsᴛ" if channel_data[2] else "✗ ʀᴇѦᴜᴇsᴛ"
            timer_status = f"ᴛɪᴍᴇʀ: {channel_data[3]}ᴍ" if channel_data[3] > 0 else "ᴛɪᴍᴇʀ: ∞"
            channel_list.append(f"• `{channel_name}` (`{channel_id}`) - {request_status}, {timer_status}")
        channels_display = "\n".join(channel_list)
    else:
        channels_display = "_ɴᴏ ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴄʜᴀɴɴᴇʟs ᴄᴏɴғɪɢᴜʀᴇᴅ_"
    msg = f"""<blockquote>✦ ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ sᴇᴛᴛɪɴɢs</blockquote>
›› **ᴄᴏɴғɪɢᴜʀᴇᴅ ᴄʜᴀɴɴᴇʟs:**
{channels_display}

__ᴜsᴇ ᴛʜᴇ ᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴀᴅᴅ ᴏʀ ʀᴇᴍᴏᴠᴇ ᴀ ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴄʜᴀɴɴᴇʟ!__
"""
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('›› ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ', 'add_fsub'), InlineKeyboardButton('›› ʀᴇᴍᴏᴠᴇ ᴄʜᴀɴɴᴇʟ', 'rm_fsub')],
        [InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^db_channels$"))
async def db_channels(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    db_chs = getattr(client, 'db_channels', {})
    if db_chs:
        channel_list = []
        for channel_id_str, channel_data in db_chs.items():
            channel_name = channel_data.get('name', 'Unknown')
            is_primary = "✓ ᴘʀɪᴍᴀʀʏ" if channel_data.get('is_primary', False) else "• sᴇᴄᴏɴᴅᴀʀʏ"
            is_active = "✓ ᴀᴄᴛɪᴠᴇ" if channel_data.get('is_active', True) else "✗ ɪɴᴀᴄᴛɪᴠᴇ"
            channel_list.append(f"• `{channel_name}` (`{channel_id_str}`)\n  {is_primary} | {is_active}")
        channels_display = "\n\n".join(channel_list)
    else:
        channels_display = "_ɴᴏ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs ᴄᴏɴғɪɢᴜʀᴇᴅ_"
    primary_db = getattr(client, 'primary_db_channel', client.db)
    msg = f"""<blockquote>✦ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs sᴇᴛᴛɪɴɢs</blockquote>
›› **ᴄᴜʀʀᴇɴᴛ ᴘʀɪᴍᴀʀʏ ᴅʙ:** `{primary_db}`
›› **ᴛᴏᴛᴀʟ ᴅʙ ᴄʜᴀɴɴᴇʟs:** `{len(db_chs)}`

**ᴄᴏɴғɪɢᴜʀᴇᴅ ᴄʜᴀɴɴᴇʟs:**
{channels_display}

__ᴜsᴇ ᴛʜᴇ ᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs!__
"""
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('›› ᴀᴅᴅ ᴅʙ ᴄʜᴀɴɴᴇʟ', 'add_db_channel'), InlineKeyboardButton('›› ʀᴇᴍᴏᴠᴇ ᴅʙ ᴄʜᴀɴɴᴇʟ', 'rm_db_channel')],
        [InlineKeyboardButton('›› sᴇᴛ ᴘʀɪᴍᴀʀʏ', 'set_primary_db'), InlineKeyboardButton('›› sᴛᴀᴛᴜs', 'toggle_db_status')],
        [InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^add_db_channel$"))
async def add_db_channel(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    msg = f"""<blockquote>✦ ᴀᴅᴅ ɴᴇᴡ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ</blockquote>
›› **ᴄᴜʀʀᴇɴᴛ ᴅʙ ᴄʜᴀɴɴᴇʟs:** `{len(getattr(client, 'db_channels', {}))}`

__sᴇɴᴅ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ (ɴᴇɢᴀᴛɪᴠᴇ ɪɴᴛᴇɢᴇʀ) ᴏғ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ ɪɴ ᴛʜᴇ ɴᴇxᴛ 60 sᴇᴄᴏɴᴅs!__

**ᴇxᴀᴍᴘʟᴇ:** `-1001234567675`
**ɴᴏᴛᴇ:** ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ!"""
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        channel_id_text = res.text.strip()
        if not channel_id_text.lstrip('-').isdigit():
            return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ ɪᴅ!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'db_channels')]]))
        channel_id = int(channel_id_text)
        db_chs = getattr(client, 'db_channels', {})
        if str(channel_id) in db_chs:
            return await query.message.edit_text(f"**✗ ᴄʜᴀɴɴᴇʟ `{channel_id}` ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴅᴅᴇᴅ!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'db_channels')]]))
        try:
            chat = await client.get_chat(channel_id)
            test_msg = await client.send_message(chat_id=channel_id, text="ᴛᴇsᴛɪɴɢ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴀᴄᴄᴇss")
            await test_msg.delete()
            channel_data = {
                'name': chat.title,
                'is_primary': len(db_chs) == 0,
                'is_active': True,
                'added_by': query.from_user.id
            }
            await client.mongodb.add_db_channel(channel_id, channel_data, client.bot_id)
            if not hasattr(client, 'db_channels'):
                client.db_channels = {}
            client.db_channels[str(channel_id)] = channel_data
            if channel_data['is_primary']:
                client.primary_db_channel = channel_id
                await client.mongodb.set_primary_db_channel(channel_id, client.bot_id)
            await query.message.edit_text(f"""**✓ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ!**

›› **ᴄʜᴀɴɴᴇʟ:** `{chat.title}`
›› **ɪᴅ:** `{channel_id}`
›› **sᴛᴀᴛᴜs:** {'ᴘʀɪᴍᴀʀʏ' if channel_data['is_primary'] else 'sᴇᴄᴏɴᴅᴀʀʏ'}""",
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'db_channels')]]))
        except Exception as e:
            await query.message.edit_text(f"**✗ ᴇʀʀᴏʀ:** `{str(e)}`",
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'db_channels')]]))
    except Exception as e:
        await query.message.edit_text(f"**✗ ᴛɪᴍᴇᴏᴜᴛ ᴏʀ ᴇʀʀᴏʀ:** `{str(e)}`",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'db_channels')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^rm_db_channel$"))
async def rm_db_channel(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    db_chs = getattr(client, 'db_channels', {})
    if not db_chs:
        return await query.message.edit_text("**❌ No database channels to remove!**",
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    msg = "<blockquote>**Remove Database Channel:**</blockquote>\n**Available Channels:**\n"
    for channel_id_str, channel_data in db_chs.items():
        channel_name = channel_data.get('name', 'Unknown')
        is_primary = " (Primary)" if channel_data.get('is_primary', False) else ""
        msg += f"• `{channel_name}` - `{channel_id_str}`{is_primary}\n"
    msg += "\n__Send the channel ID you want to remove in the next 60 seconds!__"
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        channel_id_text = res.text.strip()
        if not channel_id_text.lstrip('-').isdigit():
            return await query.message.edit_text("**❌ Invalid channel ID!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        channel_id = int(channel_id_text)
        if str(channel_id) not in db_chs:
            return await query.message.edit_text(f"**❌ Channel `{channel_id}` not found!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        if db_chs[str(channel_id)].get('is_primary', False) and len(db_chs) > 1:
            return await query.message.edit_text("**❌ Cannot remove primary channel!**\n\n__Set another channel as primary first.__",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        channel_name = db_chs[str(channel_id)].get('name', 'Unknown')
        await client.mongodb.remove_db_channel(channel_id, client.bot_id)
        del client.db_channels[str(channel_id)]
        await query.message.edit_text(f"**✅ Removed:** `{channel_name}` (`{channel_id}`)",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    except Exception as e:
        await query.message.edit_text(f"**❌ Timeout or error:** `{str(e)}`",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^set_primary_db$"))
async def set_primary_db(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    db_chs = getattr(client, 'db_channels', {})
    if not db_chs:
        return await query.message.edit_text("**❌ No database channels available!**",
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    msg = "<blockquote>**Set Primary Database Channel:**</blockquote>\n**Available Channels:**\n"
    for channel_id_str, channel_data in db_chs.items():
        channel_name = channel_data.get('name', 'Unknown')
        is_primary = " (Current Primary)" if channel_data.get('is_primary', False) else ""
        msg += f"• `{channel_name}` - `{channel_id_str}`{is_primary}\n"
    msg += "\n__Send the channel ID to set as primary in the next 60 seconds!__"
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        channel_id_text = res.text.strip()
        if not channel_id_text.lstrip('-').isdigit():
            return await query.message.edit_text("**❌ Invalid channel ID!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        channel_id = int(channel_id_text)
        if str(channel_id) not in db_chs:
            return await query.message.edit_text(f"**❌ Channel `{channel_id}` not found!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        await client.mongodb.set_primary_db_channel(channel_id, client.bot_id)
        for ch_id, ch_data in client.db_channels.items():
            ch_data['is_primary'] = (int(ch_id) == channel_id)
        client.primary_db_channel = channel_id
        client.db = channel_id
        channel_name = db_chs[str(channel_id)].get('name', 'Unknown')
        await query.message.edit_text(f"**✅ Primary DB updated!**\n\n**New Primary:** `{channel_name}` (`{channel_id}`)",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    except Exception as e:
        await query.message.edit_text(f"**❌ Timeout or error:** `{str(e)}`",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^toggle_db_status$"))
async def toggle_db_status(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    db_chs = getattr(client, 'db_channels', {})
    if not db_chs:
        return await query.message.edit_text("**❌ No database channels available!**",
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    msg = "<blockquote>**Toggle Channel Status:**</blockquote>\n**Available Channels:**\n"
    for channel_id_str, channel_data in db_chs.items():
        channel_name = channel_data.get('name', 'Unknown')
        status = "🟢 ᴀᴄᴛɪᴠᴇ" if channel_data.get('is_active', True) else "🔴 ɪɴᴀᴄᴛɪᴠᴇ"
        msg += f"• `{channel_name}` - `{channel_id_str}` ({status})\n"
    msg += "\n__Send the channel ID to toggle status in the next 60 seconds!__"
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        channel_id_text = res.text.strip()
        if not channel_id_text.lstrip('-').isdigit():
            return await query.message.edit_text("**❌ Invalid channel ID!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        channel_id = int(channel_id_text)
        if str(channel_id) not in db_chs:
            return await query.message.edit_text(f"**❌ Channel `{channel_id}` not found!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        new_status = await client.mongodb.toggle_db_channel_status(channel_id, client.bot_id)
        if new_status is not None:
            client.db_channels[str(channel_id)]['is_active'] = new_status
            channel_name = db_chs[str(channel_id)].get('name', 'Unknown')
            status_text = "🟢 Active" if new_status else "🔴 Inactive"
            await query.message.edit_text(f"**✅ Status updated!**\n\n**Channel:** `{channel_name}`\n**Status:** {status_text}",
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
        else:
            await query.message.edit_text("**❌ Failed to toggle status!**",
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))
    except Exception as e:
        await query.message.edit_text(f"**❌ Timeout or error:** `{str(e)}`",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'db_channels')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^photos$"))
async def photos(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    msg = f"""<blockquote>**Photo Settings:**</blockquote>
**Start Photo:** `{client.messages.get("START_PHOTO", "None")}`
**Force Sub Photo:** `{client.messages.get('FSUB_PHOTO', 'None')}`

__Use the buttons below to manage photos!__
"""
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(('ꜱᴇᴛ' if not client.messages.get("START_PHOTO") else 'ᴄʜᴀɴɢᴇ') + '\nꜱᴛᴀʀᴛ ᴘʜᴏᴛᴏ', callback_data='add_start_photo'),
            InlineKeyboardButton(('ꜱᴇᴛ' if not client.messages.get("FSUB_PHOTO") else 'ᴄʜᴀɴɢᴇ') + '\nꜰꜱᴜʙ ᴘʜᴏᴛᴏ', callback_data='add_fsub_photo')
        ],
        [
            InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ\nꜱᴛᴀʀᴛ ᴘʜᴏᴛᴏ', callback_data='rm_start_photo'),
            InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ\nꜰꜱᴜʙ ᴘʜᴏᴛᴏ', callback_data='rm_fsub_photo')
        ],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', callback_data='settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^protect$"))
async def protect(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    client.protect = not client.protect
    return await settings(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^auto_del$"))
async def auto_del(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    msg = f"""<blockquote>**Change Auto Delete Time:**</blockquote>
**Current Timer:** `{client.auto_del}`

__Enter new integer value (seconds). Use 0 to disable, -1 to cancel. Wait 60s to timeout!__
"""
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        timer = res.text.strip()
        if timer.lstrip('+-').isdigit():
            timer = int(timer)
            if timer >= 0:
                client.auto_del = timer
                return await query.message.edit_text(f'**Auto Delete timer changed to `{timer}` seconds!**',
                                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
            else:
                return await query.message.edit_text("**No change made to auto delete timer.**",
                                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
        else:
            return await query.message.edit_text("**That is not a valid integer!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**Timeout, try again!**",
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]]))

#===============================================================#

@Client.on_callback_query(filters.regex('^rm_start_photo$'))
async def rm_start_photo(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    client.messages['START_PHOTO'] = ''
    await query.answer()
    await photos(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex('^rm_fsub_photo$'))
async def rm_fsub_photo(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    client.messages['FSUB_PHOTO'] = ''
    await query.answer()
    await photos(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^add_start_photo$"))
async def add_start_photo(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    msg = f"""<blockquote>**Change Start Image:**</blockquote>
**Current Start Image:** `{client.messages.get('START_PHOTO', '')}`

__Send the new image or a URL (must start with https://), or wait 60s to cancel!__
"""
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=(filters.text | filters.photo), timeout=60)
        if res.text and (res.text.startswith('https://') or res.text.startswith('http://')):
            client.messages['START_PHOTO'] = res.text
            return await query.message.edit_text("**✅ Start photo link updated!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        elif res.photo:
            loc = await res.download()
            client.messages['START_PHOTO'] = loc
            return await query.message.edit_text("**✅ Start photo updated!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        else:
            return await query.message.edit_text("**❌ Invalid format! Send a photo or a https:// link.**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**Timeout, try again!**",
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^add_fsub_photo$"))
async def add_fsub_photo(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    msg = f"""<blockquote>**Change Force Sub Image:**</blockquote>
**Current Force Sub Image:** `{client.messages.get('FSUB_PHOTO', '')}`

__Send the new image or a URL (must start with https://), or wait 60s to cancel!__
"""
    await query.message.edit_text(msg)
    try:
        res = await client.listen(user_id=query.from_user.id, filters=(filters.text | filters.photo), timeout=60)
        if res.text and (res.text.startswith('https://') or res.text.startswith('http://')):
            client.messages['FSUB_PHOTO'] = res.text
            return await query.message.edit_text("**✅ FSub photo link updated!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        elif res.photo:
            loc = await res.download()
            client.messages['FSUB_PHOTO'] = loc
            return await query.message.edit_text("**✅ FSub photo updated!**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
        else:
            return await query.message.edit_text("**❌ Invalid format! Send a photo or a https:// link.**",
                                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**Timeout, try again!**",
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'photos')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^file_prefix$"))
async def file_caption_menu(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    prefix = getattr(client, 'file_prefix', '') or 'ɴᴏᴛ sᴇᴛ'
    template = getattr(client, 'file_caption_template', '') or 'ɴᴏᴛ sᴇᴛ'
    buttons = getattr(client, 'file_buttons', [])
    btn_count = sum(len(row) for row in buttons)
    msg = f"""<blockquote>✦ ꜰɪʟᴇ ᴄᴀᴘᴛɪᴏɴ sᴇᴛᴛɪɴɢs</blockquote>

ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ʙᴏᴛ ɢɪᴠᴇɴ ꜰɪʟᴇ ᴄᴀᴘᴛɪᴏɴ.

›› **ᴘʀᴇꜰɪx:** <code>{prefix}</code>
›› **ᴄᴜsᴛᴏᴍ ᴛᴇᴍᴘʟᴀᴛᴇ:** <code>{template}</code>
›› **ꜰɪʟᴇ ʙᴜᴛᴛᴏɴs:** `{btn_count} ʙᴜᴛᴛᴏɴ(s) ᴄᴏɴꜰɪɢᴜʀᴇᴅ`

__ɴᴏᴛᴇ: ɪꜰ ᴛᴇᴍᴘʟᴀᴛᴇ ɪs sᴇᴛ, ɪᴛ ᴏᴠᴇʀʀɪᴅᴇs ᴘʀᴇꜰɪx.__
__ᴜsᴇ `{{original_caption}}` ɪɴ ᴛᴇᴍᴘʟᴀᴛᴇ ᴛᴏ ɪɴᴄʟᴜᴅᴇ ᴏʀɪɢɪɴᴀʟ ꜰɪʟᴇɴᴀᴍᴇ.__"""
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('›› sᴇᴛ ᴘʀᴇꜰɪx', 'set_file_prefix'), InlineKeyboardButton('›› sᴇᴛ ᴛᴇᴍᴘʟᴀᴛᴇ', 'set_file_template')],
        [InlineKeyboardButton('›› ᴍᴀɴᴀɢᴇ ʙᴜᴛᴛᴏɴs', 'file_buttons_menu')],
        [InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^set_file_prefix$"))
async def set_file_prefix(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    current = getattr(client, 'file_prefix', '') or 'ɴᴏᴛ sᴇᴛ'
    msg = f"""<blockquote>✦ sᴇᴛ ꜰɪʟᴇ ᴘʀᴇꜰɪx</blockquote>

›› **ᴄᴜʀʀᴇɴᴛ:** <code>{current}</code>

__sᴇɴᴅ ʏᴏᴜʀ ᴘʀᴇꜰɪx ᴛᴇxᴛ. sᴇɴᴅ `0` ᴛᴏ ʀᴇᴍᴏᴠᴇ.__

**ᴇxᴀᴍᴘʟᴇ:** `@F2_Linkz`
**ʀᴇsᴜʟᴛ:** `@F2_Linkz - ꜰɪʟᴇɴᴀᴍᴇ`"""
    await query.message.edit_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_prefix')]]))
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        val = res.text.strip()
        if val == '0':
            client.file_prefix = ''
            await client.mongodb.update_bot_setting('file_prefix', '', client.bot_id)
            return await query.message.edit_text("**✓ ᴘʀᴇꜰɪx ʀᴇᴍᴏᴠᴇᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_prefix')]]))
        client.file_prefix = val
        await client.mongodb.update_bot_setting('file_prefix', val, client.bot_id)
        return await query.message.edit_text(f"**✓ ᴘʀᴇꜰɪx ᴜᴘᴅᴀᴛᴇᴅ!**\n\n›› `{val}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_prefix')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**✗ ᴛɪᴍᴇᴏᴜᴛ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_prefix')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^set_file_template$"))
async def set_file_template(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    current = getattr(client, 'file_caption_template', '') or 'ɴᴏᴛ sᴇᴛ'
    msg = f"""<blockquote>✦ sᴇᴛ ꜰɪʟᴇ ᴄᴀᴘᴛɪᴏɴ ᴛᴇᴍᴘʟᴀᴛᴇ</blockquote>

›› **ᴄᴜʀʀᴇɴᴛ:**
<pre>{current}</pre>

__sᴇɴᴅ ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴛᴇᴍᴘʟᴀᴛᴇ. sᴇɴᴅ `0` ᴛᴏ ᴄʟᴇᴀʀ.__

**ᴠᴀʀɪᴀʙʟᴇs:**
• `{{original_caption}}` — ᴏʀɪɢɪɴᴀʟ ꜰɪʟᴇɴᴀᴍᴇ (ʟɪɴᴋs sᴛʀɪᴘᴘᴇᴅ)

**ᴇxᴀᴍᴘʟᴇ ᴛᴇᴍᴘʟᴀᴛᴇ:**
<pre>@F2_Linkz - {{original_caption}}

⚡ Powered By
@Disney_Movies_Collections</pre>"""
    await query.message.edit_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_prefix')]]))
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=120)
        val = res.text.strip()
        if val == '0':
            client.file_caption_template = ''
            await client.mongodb.update_bot_setting('file_caption_template', '', client.bot_id)
            return await query.message.edit_text("**✓ ᴛᴇᴍᴘʟᴀᴛᴇ ᴄʟᴇᴀʀᴇᴅ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_prefix')]]))
        client.file_caption_template = val
        await client.mongodb.update_bot_setting('file_caption_template', val, client.bot_id)
        return await query.message.edit_text(f"**✓ ᴛᴇᴍᴘʟᴀᴛᴇ ᴜᴘᴅᴀᴛᴇᴅ!**\n\n<pre>{val}</pre>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_prefix')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**✗ ᴛɪᴍᴇᴏᴜᴛ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_prefix')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^file_buttons_menu$"))
async def file_buttons_menu(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    buttons = getattr(client, 'file_buttons', [])
    btn_list = ""
    if buttons:
        for i, row in enumerate(buttons):
            for btn in row:
                btn_list += f"• <b>{btn['text']}</b> — <code>{btn['url']}</code>\n"
    else:
        btn_list = "_ɴᴏ ʙᴜᴛᴛᴏɴs sᴇᴛ_"
    msg = f"""<blockquote>✦ ꜰɪʟᴇ ʙᴜᴛᴛᴏɴs</blockquote>

ᴛʜᴇsᴇ ʙᴜᴛᴛᴏɴs ᴀᴘᴘᴇᴀʀ ᴜɴᴅᴇʀ ᴇᴠᴇʀʏ ꜰɪʟᴇ sᴇɴᴛ ʙʏ ᴛʜᴇ ʙᴏᴛ.

**ᴄᴜʀʀᴇɴᴛ ʙᴜᴛᴛᴏɴs:**
{btn_list}"""
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('›› ᴀᴅᴅ ʙᴜᴛᴛᴏɴ', 'add_file_button'), InlineKeyboardButton('›› ᴄʟᴇᴀʀ ᴀʟʟ', 'clear_file_buttons')],
        [InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_prefix')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^add_file_button$"))
async def add_file_button(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    msg = """<blockquote>✦ ᴀᴅᴅ ꜰɪʟᴇ ʙᴜᴛᴛᴏɴ</blockquote>

__sᴇɴᴅ ʙᴜᴛᴛᴏɴ ᴅᴇᴛᴀɪʟs ɪɴ ᴛʜɪs ꜰᴏʀᴍᴀᴛ:__

<pre>Button Text | https://yourlink.com</pre>

__ᴇxᴀᴍᴘʟᴇs:__
<pre>🔔 Join Channel | https://t.me/F2_Linkz</pre>
<pre>💬 Support Group | https://t.me/+V7zUi7O_DkEyNGZl</pre>

__ᴍᴜʟᴛɪᴘʟᴇ ʙᴜᴛᴛᴏɴs ɪɴ ᴏɴᴇ ʀᴏᴡ — sᴇᴘᴀʀᴀᴛᴇ ᴡɪᴛʜ `&&`:__
<pre>Channel | https://t.me/F2_Linkz && Group | https://t.me/+V7zUi7O_DkEyNGZl</pre>"""
    await query.message.edit_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_buttons_menu')]]))
    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        raw = res.text.strip()
        parts = [p.strip() for p in raw.split('&&')]
        row = []
        for part in parts:
            if '|' not in part:
                return await query.message.edit_text("**✗ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ!** ᴜsᴇ `ᴛᴇxᴛ | ᴜʀʟ`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_buttons_menu')]]))
            text, url = part.split('|', 1)
            text, url = text.strip(), url.strip()
            if not url.startswith('http'):
                return await query.message.edit_text("**✗ ᴜʀʟ ᴍᴜsᴛ sᴛᴀʀᴛ ᴡɪᴛʜ https://**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_buttons_menu')]]))
            row.append({'text': text, 'url': url})
        if not hasattr(client, 'file_buttons') or client.file_buttons is None:
            client.file_buttons = []
        client.file_buttons.append(row)
        await client.mongodb.update_bot_setting('file_buttons', client.file_buttons, client.bot_id)
        preview = '\n'.join([' | '.join(f"[{b['text']}]" for b in r) for r in client.file_buttons])
        return await query.message.edit_text(f"**✓ ʙᴜᴛᴛᴏɴ ᴀᴅᴅᴇᴅ!**\n\n**ᴀʟʟ ʙᴜᴛᴛᴏɴs:**\n{preview}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_buttons_menu')]]))
    except ListenerTimeout:
        return await query.message.edit_text("**✗ ᴛɪᴍᴇᴏᴜᴛ!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'file_buttons_menu')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^clear_file_buttons$"))
async def clear_file_buttons(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('✗ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    client.file_buttons = []
    await client.mongodb.update_bot_setting('file_buttons', [], client.bot_id)
    await query.answer('✓ ᴀʟʟ ʙᴜᴛᴛᴏɴs ᴄʟᴇᴀʀᴇᴅ!', show_alert=True)
    await file_buttons_menu(client, query)
