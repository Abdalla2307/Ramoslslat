import asyncio, re, ast, math, logging, pyrogram
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
from utils import get_shortlink 
from info import AUTH_USERS, PM_IMDB, SINGLE_BUTTON, PROTECT_CONTENT, SPELL_CHECK_REPLY, IMDB_TEMPLATE, IMDB_DELET_TIME, PMFILTER, G_FILTER, SHORT_URL, SHORT_API, SPELL_IMG
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
                InlineKeyboardButton(f'مش لاقي المسلسل', 'معلومة'),
                InlineKeyboardButton(f'معلومة', 'مش لاقي المسلسل')
        ]
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
        cap = f"<b>المسلسل الذي بحثت عنه هو</b> {search}"
    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(btn))
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
        k = await msg.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(8)
        await k.delete()
        return
        k = await msg.reply("I couldn't find anything related to that. Check your spelling")
        await asyncio.sleep(8)
        await k.delete()
        return
    temp.SPELL_CHECK[msg.id] = movielist
    btn = [[
        InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"spolling#{user}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spolling#{user}#close_spellcheck')])
    await msg.reply("I couldn't find anything related to that\nDid you mean any one of these?")

