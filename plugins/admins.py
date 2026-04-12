from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import time
import psutil
import shutil

#===============================================================#

@Client.on_callback_query(filters.regex("^admins$"))
async def admins(client: Client, query: CallbackQuery):
    if not (query.from_user.id == client.owner):
        return await query.answer('This can only be used by the owner.', show_alert=True)
    await query.answer()
    msg = f"""<blockquote>**Admin Settings:**</blockquote>
**Admin User IDs:** {", ".join(f"`{a}`" for a in client.admins)}

__Use the appropriate button below to add or remove an admin based on your needs!__
"""
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('ᴀᴅᴅ ᴀᴅᴍɪɴ', 'add_admin'), InlineKeyboardButton('ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ', 'rm_admin')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_message(filters.command("stats"))
async def usage_cmd(client: Client, message: Message):
    if not message.from_user.id in client.admins:
        return await message.reply("✗ ᴛʜɪs ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ʙʏ ᴀᴅᴍɪɴs!")

    reply = await message.reply("<blockquote>›› ᴇxᴛʀᴀᴄᴛɪɴɢ ᴜsᴀɢᴇ ᴅᴀᴛᴀ...</blockquote>")

    try:
        total_users_list = await client.mongodb.full_userbase()
        total_users = len(total_users_list)
    except Exception:
        total_users = "ᴇʀʀᴏʀ"

    from datetime import datetime
    uptime_duration = datetime.now() - getattr(client, 'uptime', datetime.now())
    days = uptime_duration.days
    hours, remainder = divmod(uptime_duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    uptime_str = f"{days}ᴅ {hours}ʜ {minutes}ᴍ"

    total, used, free = shutil.disk_usage("/")
    total_gb = total / (1024**3)
    used_gb = used / (1024**3)
    free_gb = free / (1024**3)
    disk_percent = (used / total) * 100

    ram = psutil.virtual_memory()
    total_ram = ram.total / (1024**3)
    used_ram = ram.used / (1024**3)
    free_ram = ram.available / (1024**3)
    ram_percent = ram.percent

    swap = psutil.swap_memory()
    total_swap = swap.total / (1024**3)
    used_swap = swap.used / (1024**3)
    free_swap = swap.free / (1024**3)
    swap_percent = swap.percent

    cpu_usage = psutil.cpu_percent(interval=1)

    try:
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent / (1024**2)
        bytes_recv = net_io.bytes_recv / (1024**2)
        network_status = "✓ ᴀᴠᴀɪʟᴀʙʟᴇ"
        net_section = f"""<blockquote>›› **ᴜᴘʟᴏᴀᴅᴇᴅ:** `{bytes_sent:.2f} ᴍʙ`
›› **ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ:** `{bytes_recv:.2f} ᴍʙ`</blockquote>"""
    except PermissionError:
        network_status = "✗ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ"
        net_section = "<blockquote>›› **sᴛᴀᴛᴜs:** `ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ᴏɴ ᴘʀᴏᴏᴛ`</blockquote>"

    try:
        process = psutil.Process()
        bot_cpu_usage = process.cpu_percent(interval=1)
        bot_memory_usage = process.memory_info().rss / (1024**2)
        bot_status = "✓ ʀᴜɴɴɪɴɢ"
    except Exception:
        bot_cpu_usage = 0.0
        bot_memory_usage = 0.0
        bot_status = "✗ ᴇʀʀᴏʀ"

    disk_status = "✓ ɴᴏʀᴍᴀʟ" if disk_percent < 80 else "✗ ʜɪɢʜ" if disk_percent < 95 else "✗ ᴄʀɪᴛɪᴄᴀʟ"
    ram_status = "✓ ɴᴏʀᴍᴀʟ" if ram_percent < 80 else "✗ ʜɪɢʜ" if ram_percent < 95 else "✗ ᴄʀɪᴛɪᴄᴀʟ"
    cpu_status = "✓ ɴᴏʀᴍᴀʟ" if cpu_usage < 80 else "✗ ʜɪɢʜ" if cpu_usage < 95 else "✗ ᴄʀɪᴛɪᴄᴀʟ"

    msg = f"""<blockquote>✦ sʏsᴛᴇᴍ ᴜsᴀɢᴇ sᴛᴀᴛs</blockquote>

<blockquote><u>**≡ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs:**</u></blockquote>
<blockquote>›› **ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{total_users}`
›› **ʙᴏᴛ sᴛᴀᴛᴜs:** {bot_status}
›› **ᴜᴘᴛɪᴍᴇ:** `{uptime_str}`
›› **ᴀᴅᴍɪɴs:** `{len(client.admins)}`</blockquote>

<blockquote><u>**≡ ᴅɪsᴋ ᴜsᴀɢᴇ:**</u></blockquote>
<blockquote>›› **ᴛᴏᴛᴀʟ:** `{total_gb:.2f} ɢʙ`
›› **ᴜsᴇᴅ:** `{used_gb:.2f} ɢʙ` ({disk_percent:.1f}%)
›› **ꜰʀᴇᴇ:** `{free_gb:.2f} ɢʙ`
›› **sᴛᴀᴛᴜs:** {disk_status}</blockquote>

<blockquote><u>**≡ ʀᴀᴍ ᴜsᴀɢᴇ:**</u></blockquote>
<blockquote>›› **ᴛᴏᴛᴀʟ:** `{total_ram:.2f} ɢʙ`
›› **ᴜsᴇᴅ:** `{used_ram:.2f} ɢʙ` ({ram_percent:.1f}%)
›› **ꜰʀᴇᴇ:** `{free_ram:.2f} ɢʙ`
›› **sᴛᴀᴛᴜs:** {ram_status}</blockquote>

<blockquote><u>**≡ sᴡᴀᴘ ᴜsᴀɢᴇ:**</u></blockquote>
<blockquote>›› **ᴛᴏᴛᴀʟ:** `{total_swap:.2f} ɢʙ`
›› **ᴜsᴇᴅ:** `{used_swap:.2f} ɢʙ` ({swap_percent:.1f}%)
›› **ꜰʀᴇᴇ:** `{free_swap:.2f} ɢʙ`</blockquote>

<blockquote><u>**≡ ᴄᴘᴜ & ɴᴇᴛᴡᴏʀᴋ:**</u></blockquote>
<blockquote>›› **ᴄᴘᴜ ᴜsᴀɢᴇ:** `{cpu_usage:.2f}%` {cpu_status}
›› **ɴᴇᴛᴡᴏʀᴋ:** {network_status}</blockquote>
{net_section}

<blockquote><u>**≡ ʙᴏᴛ ʀᴇsᴏᴜʀᴄᴇ ᴜsᴀɢᴇ:**</u></blockquote>
<blockquote>›› **ᴄᴘᴜ:** `{bot_cpu_usage:.2f}%`
›› **ᴍᴇᴍᴏʀʏ:** `{bot_memory_usage:.2f} ᴍʙ`</blockquote>

<blockquote>**• ᴜsᴇ ᴛʜɪs ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴛᴏ ᴍᴏɴɪᴛᴏʀ ʏᴏᴜʀ ʙᴏᴛ's ᴘᴇʀꜰᴏʀᴍᴀɴᴄᴇ!**</blockquote>"""

    await reply.edit_text(msg)

#===============================================================#

@Client.on_callback_query(filters.regex("^add_admin$"))
async def add_new_admins(client: Client, query: CallbackQuery):
    await query.answer()
    if not query.from_user.id in client.admins:
        return await client.send_message(query.from_user.id, client.reply_text)
    ids_msg = await client.ask(query.from_user.id, "Send user ids separated by a space in the next 60 seconds!\nEg: `838278682 83622928 82789928`", filters=filters.text, timeout=60)
    ids = ids_msg.text.split()
    try:
        for identifier in ids:
            if int(identifier) not in client.admins:
                client.admins.append(int(identifier))
    except Exception as e:
        return await ids_msg.reply(f"Error: {e}")
    await admins(client, query)
    return await ids_msg.reply(f"__{len(ids)} admin {'id' if len(ids)==1 else 'ids'} have been promoted!!__")

#===============================================================#

@Client.on_callback_query(filters.regex("^rm_admin$"))
async def remove_admins(client: Client, query: CallbackQuery):
    await query.answer()
    if not query.from_user.id in client.admins:
        return await client.send_message(query.from_user.id, client.reply_text)
    ids_msg = await client.ask(query.from_user.id, "Send user ids separated by a space in the next 60 seconds!\nEg: `838278682 83622928 82789928`", filters=filters.text, timeout=60)
    ids = ids_msg.text.split()
    try:
        for identifier in ids:
            if int(identifier) == client.owner:
                await client.send_message(query.from_user.id, "Cannot remove the owner from the admin list!")
                continue
            if int(identifier) in client.admins:
                client.admins.remove(int(identifier))
    except Exception as e:
        return await ids_msg.reply(f"Error: {e}")
    await admins(client, query)
    return await ids_msg.reply(f"__{len(ids)} admin {'id' if len(ids)==1 else 'ids'} have been removed!!__")

#===============================================================#

@Client.on_message(filters.command('bl') & filters.private)
async def blacklist_cmd(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply(client.reply_text)

    args = message.text.split(None, 1)

    # /bl list
    if len(args) == 1 or args[1].strip().lower() == "list":
        bl = getattr(client, 'caption_blacklist', [])
        if not bl:
            return await message.reply("**Blacklist is empty.**")
        items = "\n".join(f"`{w}`" for w in bl)
        return await message.reply(f"**Blacklisted words:**\n{items}")

    action_text = args[1].strip()

    # /bl del (word)
    if action_text.lower().startswith("del "):
        word = action_text[4:].strip()
        bl = getattr(client, 'caption_blacklist', [])
        if word in bl:
            bl.remove(word)
            client.caption_blacklist = bl
            await client.mongodb.set_bot_setting('caption_blacklist', bl, client.bot_id)
            return await message.reply(f"Removed `{word}` from blacklist.")
        return await message.reply(f"`{word}` not in blacklist.")

    # /bl (word) — add
    word = action_text
    bl = getattr(client, 'caption_blacklist', [])
    if word in bl:
        return await message.reply(f"`{word}` already in blacklist.")
    bl.append(word)
    client.caption_blacklist = bl
    await client.mongodb.set_bot_setting('caption_blacklist', bl, client.bot_id)
    await message.reply(f"Added `{word}` to blacklist. ✅\n\nIt will be stripped from all captions.")
