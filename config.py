import logging
from logging.handlers import RotatingFileHandler

# Bot Configuration
LOG_FILE_NAME = "bot.log"
PORT = '8086'
OWNER_ID = 1461359037

MSG_EFFECT = 5159385139981059251

SHORT_URL = "" # shortner url 
SHORT_API = "" 
SHORT_TUT = ""

# Bot Configuration
SESSION = "yato"
TOKEN = "8068264764:AAFJUXGWe1C0N_M26pN1AsG7EnJj9k8NOYo"
API_ID = "35580735"
API_HASH = "5ac978532adf9c7d2c0b150fa0f492fb"
WORKERS = 5

DB_URI = "mongodb+srv://nothingsunfav8_db_user:cZjzhPcqH6dIOMrz@cluster0.xthac8f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "yato"

FSUBS = [[-1003510823697, True, 10]] # Force Subscription Channels [channel_id, request_enabled, timer_in_minutes]
# Database Channel (Primary)
DB_CHANNEL =-1002419692267  # just put channel id dont add ""
# Multiple Database Channels (can be set via bot settings)
#DB_CHANNELS = {
     "-1002419692267": {"name": "Primary DB", "is_primary": True, "is_active": True},
     "-1002419692267": {"name": "Secondary DB", "is_primary": False, "is_active": True}
 }
# Auto Delete Timer (seconds)
AUTO_DEL = 900
# Admin IDs
ADMINS = [8372956796]
# Bot Settings
DISABLE_BTN = True
PROTECT = False

# Messages Configuration
MESSAGES = {
    "START": "<b>›› ʜᴇʏ!!, {first} ~ <blockquote>I Aᴍ A Pᴇʀᴍᴀɴᴇɴᴛ Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ Aɴᴅ Mᴀɴʏ Aᴍᴀᴢɪɴɢ Aᴅᴠᴀɴᴄᴇ Fᴇᴀᴛᴜʀᴇ Aɴᴅ Usᴇʀs Cᴀɴ Aᴄᴄᴇss Sᴛᴏʀᴇᴅ Mᴇssᴀɢᴇs Bʏ Usɪɴɢ A Sʜᴀʀᴇᴀʙʟᴇ Lɪɴᴋ Gɪᴠᴇɴ Bʏ @ATXanime!!! Tᴏ Kɴᴏᴡ Mᴏʀᴇ Cʟɪᴄᴋ Hᴇʟᴘ Bᴜᴛᴛᴏɴ...</blockquote></b>",
    "FSUB": "<b><blockquote>›› ʜᴇʏ ×</blockquote>\n  ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs</b>",
    "ABOUT": "<b>›› ғᴏʀ ᴍᴏʀᴇ: @yagamiuniversse \n <blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/yagamiuniversse'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› ᴏᴡɴᴇʀ: @Leoyagamihere\n›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a> \n›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a> \n›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a> \n›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @Leoyagamihere</b></blockquote>",
    "REPLY": "<b>For More Join - @yagamiuniversse</b>",
    "SHORT_MSG": "<b>📊 ʜᴇʏ {first}, \n\n‼️ ɢᴇᴛ ᴀʟʟ ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʟɪɴᴋ ‼️\n\n ⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>",
    "START_PHOTO": "https://i.ibb.co/HDShbV4v/photo-2025-12-17-09-44-02-7584760452001824820.jpg",
    "FSUB_PHOTO": "https://i.ibb.co/LhX80sRn/photo-2025-12-17-09-30-13-7584757509949227064.jpg",
    "SHORT_PIC": "https://i.ibb.co/mFvVYnrR/photo-2025-12-17-09-30-06-7584757509949227052.jpg",
    "SHORT": "https://i.ibb.co/Y769JWL1/photo-2025-12-17-09-31-45-7584757509949227048.jpg"
}

def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt='%d-%b-%y %H:%M:%S'
    )
    file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
