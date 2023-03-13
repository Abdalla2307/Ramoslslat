import re
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]:
        return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Bot information
PORT = environ.get("PORT", "8080")
WEBHOOK = bool(environ.get("WEBHOOK", True)) # for web support on/off
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS' ,'https://telegra.ph/file/cd555b1619d8416a137dc.jpg https://telegra.ph/file/d0f17ea57380d055d50de.jpg https://telegra.ph/file/f31eb15d5249975be393a.jpg https://telegra.ph/file/d0f17ea57380d055d50de.jpg https://telegra.ph/file/f31eb15d5249975be393a.jpg https://telegra.ph/file/d75d05854a7081145e57a.jpg https://telegra.ph/file/a70e97c1a89bcb0fd7d30.jpg https://telegra.ph/file/1e4a0eb1b735dbc46d43d.jpg https://telegra.ph/file/dddcca9670620d13dcd67.jpg https://telegra.ph/file/62044a3c72ddfdeae1fbc.jpg https://telegra.ph/file/54e6a02b5a590100fcf47.jpg https://telegra.ph/file/d7a36f22fcbb8d864c7e3.jpg https://telegra.ph/file/c0080abe6b043adc34831.jpg https://telegra.ph/file/cb59c2886ccf73b615eaf.jpg https://telegra.ph/file/a5c0e349f01b0871c8594.jpg https://telegra.ph/file/9ec0d512fc3900a0f27ff.jpg https://telegra.ph/file/ad2c9e313af9098fdf907.jpg https://telegra.ph/file/d33562eb9ecc5c5086076.jpg https://telegra.ph/file/c7bf1627347b452f9c2a3.jpg https://telegra.ph/file/87a3def12517c32ee48d0.jpg https://telegra.ph/file/576570e427f27a40776d7.jpg https://telegra.ph/file/7a4a51260c6eccb792b37.jpg https://telegra.ph/file/6e14cfb77aa0d94c170d3.jpg https://telegra.ph/file/91a86d0434f0c66df5030.jpg https://telegra.ph/file/3cdc32dc7e9bf36a47499.jpg https://telegra.ph/file/62ae0f2d028ee997e62d6.jpg https://telegra.ph/file/ad5b12b504d5f7c6185e1.jpg https://telegra.ph/file/3cf62a4693d37c3520050.jpg https://telegra.ph/file/d1c00bfac5461c5f29a32.jpg https://telegra.ph/file/80c9db1b4b63107c6edf3.jpg https://telegra.ph/file/193a326c4953caa74bef3.jpg https://telegra.ph/file/e0809dfa1baef28ea8f44.jpg https://telegra.ph/file/402ca37558addb903f64c.jpg')).split()
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '324012925').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "5"))
START_MESSAGE = environ.get('START_MESSAGE', '👋 𝙷𝙴𝙻𝙾 {user}\n\nبوت لــ{bot},\nفقط اكتب اسم المسلسل هنا وسوف ارسله لك')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "⚠️ 𝙃𝙚𝙮 {query}! 𝙏𝙝𝙖𝙩'𝙨 𝙉𝙤𝙩 𝙁𝙤𝙧 𝙔𝙤𝙪. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙍𝙚𝙦𝙪𝙚𝙨𝙩 𝙔𝙤𝙪𝙧 𝙊𝙬𝙣")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', 'يرجي الاشترك في القناة لاستخدام البوت')
RemoveBG_API = environ.get("RemoveBG_API", "")
WELCOM_PIC = environ.get("WELCOM_PIC", "")
PMFILTER = environ.get('PMFILTER', "True")
G_FILTER = bool(environ.get("G_FILTER", True))
BUTTON_LOCK = environ.get("BUTTON_LOCK", "False")

# url shortner
SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")

# Others
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "600"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'ArrowFlix Discussion | Series & Movies')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
PM_IMDB = environ.get('PM_IMDB', "False")
IMDB = is_enabled((environ.get('IMDB', "False")), False)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<code>{file_caption}</code>\n\n⚙️ <b>الـحـجـم</b> {file_size}\n||👋 مرحبا {mention} لاتنسي متابعتنا||\n\n❍<b>[مسلسلات رمضان](https://t.me/MoslslatRamadan_2023)</b>\n❍<b>[جـروب الــطـلبـات](https://t.me/RamadanTV2023)</b>")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", "<code>{file_caption}</code>\n\n⚙️ <b>الـحـجـم</b> {file_size}\n||👋 مرحبا {mention} لاتنسي متابعتنا||\n\n❍<b>[مسلسلات رمضان](https://t.me/MoslslatRamadan_2023)</b>\n❍<b>[جـروب الــطـلبـات](https://t.me/RamadanTV2023)</b>")
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "🔮 ᴛɪᴛᴛʟᴇ : <a href={url}>{title}</a>\n📆 ʏᴇᴀʀ : {year}\n🎭 ɢᴇɴʀᴇ : {genres}\n🌟 ʀᴀᴛɪɴɢ : <a href={url}/ratings>{rating} IMDB</a>\n⏰ ʀᴜɴᴛɪᴍᴇ : {runtime} 𝙼𝚒𝚗𝚞𝚝𝚎𝚜\n🔹 sᴇᴀsᴏɴs : {seasons}\n🎙️ ʟᴀɴɢᴜᴀɢᴇ : {languages}\n🌍 ᴄᴏᴜɴᴛʀɪᴇs : {countries}\n📝 sᴛᴏʀʏ : {plot} \n\n  ⚡️Pᴏᴡᴇʀᴇᴅ Bʏ : <a href=https://t.me/TorrentSeriess><b>AʀʀᴏᴡFʟɪx</b></a>")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
PM_SPELL_CHECK = is_enabled(environ.get("PM_SPELL_CHECK", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "False")), False)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)


