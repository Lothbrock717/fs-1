from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.pyromod import ListenerTimeout
from helper.helper_func import is_bot_admin

#===============================================================#
# Forced FSUB: one list shared by EVERY bot that uses the same DB.
#  - Add  -> channel is added as fsub on all linked bots (and un-banned if it was banned)
#  - Ban  -> channel is removed from all linked bots and stays banned until it is
#            added again here. Linked bots pick changes up within ~30 seconds.
#===============================================================#

async def _menu(client, query):
    forced = await client.mongodb.get_forced_fsub()
    banned = await client.mongodb.get_banned_fsub()

    if forced:
        forced_txt = "\n".join(
            f"• `{(d[0] or 'Unknown')}` (`{cid}`) - {'Request: ✅' if d[2] else 'Request: ❌'}, "
            f"{('Timer: ' + str(d[3]) + 'm') if d[3] > 0 else 'Timer: ∞'}"
            for cid, d in forced.items()
        )
    else:
        forced_txt = "_None_"
    banned_txt = "\n".join(f"• `{cid}`" for cid in banned) if banned else "_None_"

    msg = f"""<blockquote>**Forced FSUB (all linked bots):**</blockquote>
**Forced channels:**
{forced_txt}

**Banned channels:**
{banned_txt}

__Add = force this channel on every bot using this DB.
Ban = remove it from every bot and keep it banned until you add it again.__
"""
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('›› ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ', 'add_forced_fsub'), InlineKeyboardButton('›› ʙᴀɴ ᴄʜᴀɴɴᴇʟ', 'ban_forced_fsub')],
        [InlineKeyboardButton('‹ ʙᴀᴄᴋ', 'fsub')]
    ])
    await query.message.edit_text(msg, reply_markup=markup)


def _owner_only(client, query):
    return query.from_user.id == client.owner


#===============================================================#

@Client.on_callback_query(filters.regex('^forced_fsub$'))
async def forced_fsub_menu(client: Client, query: CallbackQuery):
    if not _owner_only(client, query):
        return await query.answer('✗ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    await client.sync_fsub()
    await _menu(client, query)


@Client.on_callback_query(filters.regex('^add_forced_fsub$'))
async def add_forced_fsub(client: Client, query: CallbackQuery):
    if not _owner_only(client, query):
        return await query.answer('✗ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    try:
        ask = await client.ask(
            query.from_user.id,
            "Send channel id, request (yes/no), timer in minutes (0 = no expiry) separated by a space in the next 60 seconds!\n"
            "<blockquote>Eg: `-10089479289 yes 5`\n\n__This channel will be forced on every bot using this DB. "
            "If it was banned before, the ban is lifted.__</blockquote>",
            filters=filters.text, timeout=60
        )
    except ListenerTimeout:
        return
    try:
        channel_id, request, timer = ask.text.split()
        channel_id = int(channel_id)
        if request.lower() in ('true', 'on', 'yes'):
            request = True
        elif request.lower() in ('false', 'off', 'no'):
            request = False
        else:
            raise Exception("Invalid request value, use yes/no.")
        if not timer.isdigit():
            raise Exception("Timer is not a valid integer.")
        timer = int(timer)

        val, res = await is_bot_admin(client, channel_id)
        if not val:
            return await ask.reply(f"**Error:** `{res}`")

        name = (await client.get_chat(channel_id)).title
        link = None
        if timer == 0:
            link = (await client.create_chat_invite_link(channel_id, creates_join_request=request)).invite_link

        await client.mongodb.add_forced_fsub(channel_id, [name, link, request, timer])
        await client.sync_fsub()
        await _menu(client, query)
        return await ask.reply(
            f"__`{name.strip()}` is now a forced fsub channel for all linked bots "
            f"(they pick it up within ~30s; each bot must be admin in the channel).__"
        )
    except Exception as e:
        return await ask.reply(f"**Error:** `{e}`")


@Client.on_callback_query(filters.regex('^ban_forced_fsub$'))
async def ban_forced_fsub(client: Client, query: CallbackQuery):
    if not _owner_only(client, query):
        return await query.answer('✗ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!', show_alert=True)
    await query.answer()
    try:
        ask = await client.ask(
            query.from_user.id,
            "Send the channel id to ban in the next 60 seconds!\n"
            "<blockquote>__It will be removed from the fsub list of every bot using this DB and stay banned "
            "until you add it again from Forced FSUB.__</blockquote>",
            filters=filters.text, timeout=60
        )
    except ListenerTimeout:
        return
    try:
        channel_id = int(ask.text.strip())
        await client.mongodb.ban_fsub_channel(channel_id)
        await client.sync_fsub()
        await _menu(client, query)
        return await ask.reply(f"__Channel `{channel_id}` is banned and removed from all linked bots (within ~30s).__")
    except Exception as e:
        return await ask.reply(f"**Error:** `{e}`")
