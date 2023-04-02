import os, math, logging
import logging.config
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
#from Telethroid import started_telethroid
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, PORT, WEBHOOK
from utils import temp, __repo__, __license__, __copyright__
from typing import Union, Optional, AsyncGenerator
from pyrogram import types, raw
from datetime import datetime
from pytz import timezone
from pyrogram.errors import BadRequest, Unauthorized

if WEBHOOK:
    from plugins import web_server 
    from aiohttp import web

# Get logging configurations
logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)
TIMEZONE = (os.environ.get("TIMEZONE", "Asia/Kolkata"))

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=300,
            plugins={"root": "plugins"},
            sleep_threshold=10,
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats        
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        temp.B_LINK = me.mention
        self.username = '@' + me.username
        curr = datetime.now(timezone(TIMEZONE))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        if WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()
            bind_address = "0.0.0.0"
            await web.TCPSite(app, bind_address, PORT).start()
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        #started_telethroid() # installation Telethroid Library   
        if LOG_CHANNEL:
            try:
                await self.send_message(LOG_CHANNEL, text=f"<b>{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!\n\n📅 Dᴀᴛᴇ : <code>{date}</code>\n⏰ Tɪᴍᴇ : <code>{time}</code>\n🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>{TIMEZONE}</code>\n\n🉐 Vᴇʀsɪᴏɴ : <code>v{__version__} (Layer {layer})</code></b>")  # Repo : {__repo__}\n Copyright : {__copyright__}           
            except Unauthorized:             
                LOGGER.warning("Bot isn't able to send message to LOG_CHANNEL")
            except BadRequest as e:
                LOGGER.error(e)
                                         
class GetChatJoinRequests:
    async def get_chat_join_requests(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0,
        query: str = ""
    ) -> Optional[AsyncGenerator["types.ChatJoiner", None]]:
    async def stop(self, *args):
        await super().stop()
        me = await self.get_me()
        logging.info(f"{me.first_name} is_...  ♻️Restarting...")

    async def iter_messages(self, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:                       
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        offset_date = 0
        offset_user = raw.types.InputUserEmpty()

        while True:
            r = await self.invoke(
                raw.functions.messages.GetChatInviteImporters(
                    peer=await self.resolve_peer(chat_id),
                    limit=limit,
                    offset_date=offset_date,
                    offset_user=offset_user,
                    requested=True,
                    q=query
                )
            )

            if not r.importers:
                break

            users = {i.id: i for i in r.users}

            offset_date = r.importers[-1].date
            offset_user = await self.resolve_peer(r.importers[-1].user_id)

            for i in r.importers:
                yield types.ChatJoiner._parse(self, i, users)

                current += 1

                if current >= total:
                    return


pyrogram
/
pyrogram
Public
Code
Issues
101
Pull requests
54
Actions
Security
Insights
pyrogram/pyrogram/methods/invite_links/approve_all_chat_join_requests.py
@delivrance
delivrance Add usable-by labels for methods
 1 contributor
55 lines (46 sloc)  1.85 KB
#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram import raw


class ApproveAllChatJoinRequests:
    async def approve_all_chat_join_requests(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        invite_link: str = None
    ) -> bool:
        """Approve all pending join requests in a chat.
        .. include:: /_includes/usable-by/users-bots.rst
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
            invite_link (``str``, *optional*):
                Pass an invite link to approve only its join requests.
                By default, all join requests are approved.
        Returns:
            ``bool``: True on success.
        """
        await self.invoke(
            raw.functions.messages.HideAllChatJoinRequests(
                peer=await self.resolve_peer(chat_id),
                approved=True,
                link=invite_link
            )
        )

        return True
        
app = Bot()
app.run()


class GetChatJoinRequests:
    async def get_chat_join_requests(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0,
        query: str = ""
    ) -> Optional[AsyncGenerator["types.ChatJoiner", None]]:
        """Get the pending join requests of a chat.
        .. include:: /_includes/usable-by/users-bots.rst
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).
            limit (``int``, *optional*):
                Limits the number of invite links to be retrieved.
                By default, no limit is applied and all invite links are returned.
            query (``str``, *optional*):
                Query to search for a user.
        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.ChatJoiner` objects.
        Yields:
            :obj:`~pyrogram.types.ChatJoiner` objects.
        """
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        offset_date = 0
        offset_user = raw.types.InputUserEmpty()

        while True:
            r = await self.invoke(
                raw.functions.messages.GetChatInviteImporters(
                    peer=await self.resolve_peer(chat_id),
                    limit=limit,
                    offset_date=offset_date,
                    offset_user=offset_user,
                    requested=True,
                    q=query
                )
            )

            if not r.importers:
                break

            users = {i.id: i for i in r.users}

            offset_date = r.importers[-1].date
            offset_user = await self.resolve_peer(r.importers[-1].user_id)

            for i in r.importers:
                yield types.ChatJoiner._parse(self, i, users)

                current += 1

                if current >= total:
                    return

