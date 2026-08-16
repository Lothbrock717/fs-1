import logging
from logging.handlers import RotatingFileHandler

# Bot Configuration
LOG_FILE_NAME = "bot.log"
PORT = '8080'
OWNER_ID = 8235920952

MSG_EFFECT = 5159385139981059251

SHORT_URL = "" # shortner url 
SHORT_API = "" 
SHORT_TUT = ""

# Bot Configuration
SESSION = ""
TOKEN = ""
API_ID = ""
API_HASH = ""
WORKERS = 10

DB_URI = ""
DB_NAME = ""

FSUBS = [[-1003597446654, False, 10]] # Force Subscription Channels [channel_id, request_enabled, timer_in_minutes]
# Database Channel (Primary)
DB_CHANNEL =  # just put channel id dont add ""
# Multiple Database Channels (can be set via bot settings)
#DB_CHANNELS = {
#     "-1002419692267": {"name": "Primary DB", "is_primary": True, "is_active": True},
#     "-1002419692267": {"name": "Secondary DB", "is_primary": False, "is_active": True}
#}

# Auto Delete Timer (seconds)
AUTO_DEL = 900
# Log Channel (new user notifications) — set to None to disable
LOG_CHANNEL = -1002911675489

# Admin IDs
ADMINS = [8235920952]
# Bot Settings
DISABLE_BTN = True
PROTECT = False

# Messages Configuration
MESSAGES = {
    "START": "<b>›› ʜᴇʏ!!, {first} ~\nI Aᴍ A Pᴇʀᴍᴀɴᴇɴᴛ Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ Aɴᴅ Mᴀɴʏ Aᴍᴀᴢɪɴɢ Aᴅᴠᴀɴᴄᴇ Fᴇᴀᴛᴜʀᴇ Aɴᴅ Usᴇʀs Cᴀɴ Aᴄᴄᴇss Sᴛᴏʀᴇᴅ Mᴇssᴀɢᴇs Bʏ Usɪɴɢ A Sʜᴀʀᴇᴀʙʟᴇ Lɪɴᴋ Gɪᴠᴇɴ Bʏ @F2_Linkz!!! Tᴏ Kɴᴏᴡ Mᴏʀᴇ Cʟɪᴄᴋ Hᴇʟᴘ Bᴜᴛᴛᴏɴ...</b>",
    "FSUB": "<b><blockquote>›› ʜᴇʏ ×</blockquote>\n  ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs\n\nᴊᴏɪɴ ᴛʜᴇ ʙᴇʟᴏᴡ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴄʟɪᴄᴋ ᴛʀʏ ᴀɢᴀɪɴ</b>",
    "ABOUT": "<b>›› ғᴏʀ ᴍᴏʀᴇ: @F2_Linkz \n›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/+r-ez-AY7i3djNmM1'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› sᴜᴘᴘᴏʀᴛ: <a href='https://t.me/+V7zUi7O_DkEyNGZl'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› ᴏᴡɴᴇʀ: @F2_Adminn</b>",
    "REPLY": "<b>For More Join - @F2_Linkz</b>",
    "SHORT_MSG": "<b>📊 ʜᴇʏ {}, \n\n‼️ ɢᴇᴛ ᴀʟʟ ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʟɪɴᴋ ‼️\n\n ⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>",
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
