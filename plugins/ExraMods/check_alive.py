import time
import random
from pyrogram import Client, filters

CMD = ["/", "."]

@Client.on_message(filters.command("help", CMD))
async def check_alive(_, message):
    await message.reply_text("<b>𝟷. تــأكد ان البوت خاص بالمسلسل <a href=https://t.me/MoslslatRamadan_2023/5>(قـائمة البوتـات)</a>\n\n𝟸. تــأكد من كتابة المسلسل بالطريقة الصحيحة مثل\n<i>  مسلسل الكبير - مسلسل الاجهر - مسلسل الطيارة</i>\n\n𝟹. لو مش لاقي المسلسل او فيه مشكلة تواصل معنا. \nhttps://t.me/RamadanTV2023</b>")


@Client.on_message(filters.command("ping", CMD))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")
