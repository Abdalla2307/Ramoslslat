import time
import random
from pyrogram import Client, filters

CMD = ["/", "."]

@Client.on_message(filters.command("help", CMD))
async def check_alive(_, message):
    await message.reply_text("<b>1. تــأكد من كتابة المسلسل بالطريقة الصحيحة مثل\n<i>  مسلسل الكبير - مسلسل الاجهر - مسلسل الطيارة</i>\n\n2. اكتب اسم المسلسل في جروب <a href=https://t.me/RamadanTV0>(البـحـث)</a>\n\n3. تخطي الرابط للمشاهدة <a href=https://t.me/El3omdaBot?start=BATCH-BQADBAADIBEAAsPvIVEHdGLWl5kaHxYE(طريقة تخطي الرابط)</a></b>")


@Client.on_message(filters.command("ping", CMD))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")
