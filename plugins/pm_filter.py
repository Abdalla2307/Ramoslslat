import asyncio, re, ast, math, logging, pyrogram
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
from utils import get_shortlink 
from info import AUTH_USERS, PM_IMDB, SINGLE_BUTTON, PROTECT_CONTENT, SPELL_CHECK_REPLY, PM_SPELL_CHECK, IMDB_TEMPLATE, IMDB_DELET_TIME, PMFILTER, G_FILTER, SHORT_URL, SHORT_API
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums 
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from plugins.group_filter import global_filters

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.private & filters.text & filters.chat(AUTH_USERS) if AUTH_USERS else filters.text & filters.private)
async def auto_pm_fill(b, m):
    if PMFILTER.strip().lower() in ["true", "yes", "1", "enable", "y"]:       
        if G_FILTER:
            kd = await global_filters(b, m)
            if kd == False:
                await pm_AutoFilter(b, m)
        else:      
            await pm_AutoFilter(b, m)
    elif PMFILTER.strip().lower() in ["false", "no", "0", "disable", "n"]:
        return 


async def pm_AutoFilter(client, msg, pmspoll=False):    
    if not pmspoll:
        message = msg   
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:               
                return await pm_spoll_choker(msg)        
        else:
            return 
    else:
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = pmspoll
    pre = 'pmfilep' if PROTECT_CONTENT else 'pmfile'

    if SHORT_URL and SHORT_API:          
        if SINGLE_BUTTON:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=pre_{file.file_id}"))] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=pre_{file.file_id}")),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=pre_{file.file_id}"))] for file in files ]
    else:        
        if SINGLE_BUTTON:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}')] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", callback_data=f'{pre}#{req}#{file.file_id}'),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", callback_data=f'{pre}#{file.file_id}')] for file in files ]    

    btn.insert(0,
        [
                InlineKeyboardButton(f'🎬 {search} 🎬', 'rkbtn')        ]
    )

    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        temp.PM_BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"📄 𝗣𝗮𝗴𝗲 1/{math.ceil(int(total_results) / 6)}", callback_data="pages"),
            InlineKeyboardButton(text="⏩ الحلقات القديمة", callback_data=f"pmnext_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="📄 𝗣𝗮𝗴𝗲 1/1", callback_data="pages")]
        )
    if PM_IMDB.strip().lower() in ["true", "yes", "1", "enable", "y"]:
        imdb = await get_poster(search)
    else:
        imdb = None
    TEMPLATE = IMDB_TEMPLATE
    if imdb:
        cap = TEMPLATE.format(
            group = message.chat.title,
            requested = message.from_user.mention,
            query = search,
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        cap = f"<b><i>المسلسل الذي بحثت عنه هو</i></b> {search}"
    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo="https://telegra.ph/file/d2394df3f3e83f9f73c2c.jpg", caption=cap, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(IMDB_DELET_TIME)
            await hehe.delete()            
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            hmm = await message.reply_photo(photo=poster, caption=cap, reply_markup=InlineKeyboardMarkup(btn))           
            await asyncio.sleep(IMDB_DELET_TIME)
            await hmm.delete()            
        except Exception as e:
            logger.exception(e)
            cdp = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(IMDB_DELET_TIME)
            await cdp.delete()
    else:
        abc = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(IMDB_DELET_TIME)
        await abc.delete()        
    if pmspoll:
        await msg.message.delete()


async def pm_spoll_choker(msg):
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(8)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(
        r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
        '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                         re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
        for mv in g_s:
            match = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist))  # removing duplicates
    if not movielist:
        k = await msg.reply("تــأكد من كتابة اسم المسلسل صحيح\n    ⚡اضغط علي اسم المسلسل للنسخ⚡\n❍ <code>مسلسل الكبير اوي 7</code> ❍ <code>مسلسل سوق الكانتو</code>\n❍ <code>مسلسل رمضان كريم 2</code> ❍ <code>مسلسل اكس لانس</code>\n❍ <code>مسلسل كامل العدد</code> ❍ <code>مسلسل العمدة</code>\n❍ <code>مسلسل سره الباتع</code> ❍ <code>مسلسل بابا المجال</code>\n❍ <code>مسلسل الاجهر</code> ❍ <code>مسلسل ضرب نار</code>\n❍ <code>مسلسل الهرشة السابعة</code> ❍ <code>مسلسل الصفارة</code> \n❍ <code>مسلسل الكتيبة 101</code> ❍ <code>مسلسل رسالة الامام</code>\n❍ <code>مسلسل رشيد</code> ❍ <code>مسلسل عمله نادره</code>\n❍ <code>مسلسل المداح 3</code> ❍ <code>مسلسل وأخيرًا</code>\n❍ <code>مسلسل كشف مستعجل</code> ❍ <code>مسلسل الصندوق</code> \n❍ <code>مسلسل الزند ذئب العاصي</code> ❍ <code>مسلسل جت سليمة</code>\n❍ <code>مسلسل تحت الوصايا</code> ❍ <code>مسلسل تغيير جو</code>\n❍ <code>مسلسل تلت التلاته</code> ❍ <code>رامز نيفر اند</code>\n❍ <code>مسلسل ألف حمد لله علي السلامة</code>\n❍ <code>مسلسل ابتسم أيها الجنرال</code>\n       ➲ ➲ @RamadanTV3  الجروب الاحتياطي </b>",reply_to_message_id=msg.id)
        await asyncio.sleep(100)
        await k.delete()
        return
    temp.PM_SPELL_CHECK[msg.id] = movielist
    btn = [[InlineKeyboardButton(text=movie.strip(), callback_data=f"pmspolling#{user}#{k}")] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'pmspolling#{user}#close_spellcheck')])
    await msg.reply("تــأكد من كتابة اسم المسلسل صحيح\n    ⚡اضغط علي اسم المسلسل للنسخ⚡\n❍ <code>مسلسل الكبير اوي 7</code> ❍ <code>مسلسل سوق الكانتو</code>\n❍ <code>مسلسل رمضان كريم 2</code> ❍ <code>مسلسل اكس لانس</code>\n❍ <code>مسلسل كامل العدد</code> ❍ <code>مسلسل العمدة</code>\n❍ <code>مسلسل سره الباتع</code> ❍ <code>مسلسل بابا المجال</code>\n❍ <code>مسلسل الاجهر</code> ❍ <code>مسلسل ضرب نار</code>\n❍ <code>مسلسل الهرشة السابعة</code> ❍ <code>مسلسل الصفارة</code> \n❍ <code>مسلسل الكتيبة 101</code> ❍ <code>مسلسل رسالة الامام</code>\n❍ <code>مسلسل رشيد</code> ❍ <code>مسلسل عمله نادره</code>\n❍ <code>مسلسل المداح 3</code> ❍ <code>مسلسل وأخيرًا</code>\n❍ <code>مسلسل كشف مستعجل</code> ❍ <code>مسلسل الصندوق</code> \n❍ <code>مسلسل الزند ذئب العاصي</code> ❍ <code>مسلسل جت سليمة</code>\n❍ <code>مسلسل تحت الوصايا</code> ❍ <code>مسلسل تغيير جو</code>\n❍ <code>مسلسل تلت التلاته</code> ❍ <code>رامز نيفر اند</code>\n❍ <code>مسلسل ألف حمد لله علي السلامة</code>\n❍ <code>مسلسل ابتسم أيها الجنرال</code>\n       ➲ ➲ @RamadanTV3  الجروب الاحتياطي </b>",reply_to_message_id=msg.id)
