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
PICS = (environ.get('PICS' ,'https://telegra.ph/file/24d1159b8b5cf3d2cad26.jpg https://telegra.ph/file/b09e8ada80d86b57f5f99.jpg https://telegra.ph/file/e9481e32e1a4dfa534f43.jpg')).split()
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
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
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "6"))
START_MESSAGE = environ.get('START_MESSAGE', '<b>👋 مرحبا بك {user} في بوت مسلسلات رمضان 2023\n\nهذا البوت خاص بــ</b>\n\n<code>مسلسل الكبير</code> - <code>مسلسل رمضان كريم</code>\n<code>مسلسل الصفارة</code> - <code>مسلسل اكس لانس</code>\n<code>مسلسل كامل العدد</code> - <code>رامز نيفر اند</code></i>\n\nلباقي المسلسلات </b><a href=https://t.me/MoslslatRamadan_2023/29><b>اضغط هنا</b></a>')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "⚠️ 𝙃𝙚𝙮 {query}! 𝙏𝙝𝙖𝙩'𝙨 𝙉𝙤𝙩 𝙁𝙤𝙧 𝙔𝙤𝙪. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙍𝙚𝙦𝙪𝙚𝙨𝙩 𝙔𝙤𝙪𝙧 𝙊𝙬𝙣")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', "<a><b>⚠️ <u>لاستخدام البوت يرجي تخطي الرابط</u></b> ⚠️\n<code> 𝟭 اضغط علي 'استخدام البوت' من الزر\n 𝟮 يظهر لك رابط اضغط فتح\n 𝟯 بعد تخطي الرابط يرسل قناة اضغط انضمام\n 𝟰 بعدها استخدم البوت مجانا اكثر من 25 مسلسل</code></a>\n<i>       <u>💥تخطي الرابط مرة واحده فقط💥</u></i>")
RemoveBG_API = environ.get("RemoveBG_API", "")
WELCOM_PIC = environ.get("WELCOM_PIC", "")
PMFILTER = environ.get('PMFILTER', "True")
G_FILTER = bool(environ.get("G_FILTER", True))
BUTTON_LOCK = environ.get("BUTTON_LOCK", "False")

# url shortner
SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")

# Others
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "700"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'ArrowFlix Discussion | Series & Movies')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
PM_IMDB = environ.get('PM_IMDB', "False")
IMDB = is_enabled((environ.get('IMDB', "False")), False)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>{file_name}</b>\n\n⚙️ <b>الـحـجـم</b> {file_size}\n\n||👋 مرحبا {mention} لاتنسي مشاركة الجروب||\n❍ <b>[جـروب البحث 🔍](https://t.me/RamadanTV0)</b>\n❍ <b>[مسلسلات رمضان 🌙](https://t.me/ElKberAwyBot)</b>")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", "")
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "✅ <b>المسلسل جاهز\n\n⚡ الحلقات الجديدة هتنزل يوميا لو مش لاقيها استني شوية وابحث تاني\n\n🔗 بعد تخطي الرابط يرسل لك البوت الحلقه\n\n<a href=https://t.me/Ramadan_Series7/><b>لمشاهدة الحلقات القديمة كاملة اضغط هنا</b></a></b>")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
PM_SPELL_CHECK = is_enabled(environ.get("PM_SPELL_CHECK", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "False")), False)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)


