import os
import discord
import random
from datetime import datetime, timedelta
from discord.ext import commands
from discord import Activity, ActivityType

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", ".")

if not TOKEN:
    raise ValueError("❌ DISCORD_TOKEN nerastas!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

user_cooldowns = {}

media_folder = "images"
media_messages = {
    "1.png": "Šiandien tu chill kmr pakrites ant akmens VITAS 😉",
    "2.png": "Šiandien tu kraujuojantis lele VITAS 🩸",
    "3.png": "Šiandien tu norintis klausimų VITAS ❓",
    "4.png": "Šiandien tu jureivis GABRIUS 🚢",
    "5.png": "Šiandien tu pozuojantis MARKA 🤟",
    "6.png": "Šiandien tu bananinis VITAS 🍌",
    "7.png": "Šiandien tu pripises, bet laimingas MARKA 🙂",
    "8.png": "Šiandien tu pasimetes MARKA 🫠",
    "9.png": "Šiandien tu pripises ir nesigaudantis MARKA 🥴",
    "10.png": "Šiandien tu pripises ir bbz koks MARKA 🥴",
    "11.png": "Šiandien tu su surikais MARKA 👓",
    "12.png": "Šiandien tu pripises su kepuriuku MARKA 🧢",
    "13.png": "Šiandien tu laimingas prie jamesono MARKA 🍾",
    "14.png": "Šiandien tu AdomaRuojus MARKA 🤘",
    "15.png": "Šiandien tu tusofcikas su surikais MARKA 👓",
    "16.png": "Šiandien tu nesigaudantis MARKA 🤔",
    "17.png": "Šiandien tu pakvaises MARKA 🤪",
    "18.png": "Šiandien tu stadija-koma MARKA 🫨",
    "19.png": "Šiandien tu geroj stadijoj MARKA 🤗",
    "20.png": "Šiandien tu tj leksiu namo, nors balius katik prasidejo MARKA 👋",
    "21.png": "Šiandien tu bandantis nusitraukti, bet sunkiai sekasi VITAS 😠",
    "22.png": "Šiandien tu narkamanas KOSTAS 😶‍🌫️",
    "23.png": "Šiandien tu grybautojas VERSIS 🍄",
    "24.png": "Šiandien tu gaudantis išganyma MARKA 👼🏿",
    "25.png": "Šiandien tu išvarai demonus MARKA 😈",
    "26.png": "Šiandien tu truopnas vyrs EDIS 😎",
    "27.png": "Šiandien tu pisi siurpo su pantalonais JOKŪBS 🩲",
    "28.png": "Šiandien tu deklamuoji eilerašti, nes po baidariu dar neatleidzia MARKA 👂",
    "29.png": "Šiandien tu norintis pisti siurpo MYKA 💪",
    "30.png": "Šiandien tu išskrides LUKAS 🪽",
    "31.png": "Šiandien tu prie dievo LUKAS 🙏🏿",
    "32.png": "Šiandien tu gauni šiurpo LUKAS 🥹",
    "33.png": "Šiandien tu baudi tubzika MYKA 🤮",
    "34.png": "Šiandien tu tuoj varysi vemt MYKA 🫡",
    "35.png": "Šiandien tu ohota i rybalka LUKAs 🐟",
}

available_media = list(media_messages.keys())

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=Activity(type=ActivityType.playing, name="rašyk : .sarasas")
    )
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="koks")
async def koks(ctx):
    user_id = ctx.author.id
    now = datetime.utcnow()

    last_used = user_cooldowns.get(user_id)
    if last_used:
        passed = now - last_used
        cooldown = timedelta(hours=24)

        if passed < cooldown:
            remaining = cooldown - passed
            await ctx.send(
                f"❌ Kas per daug tas nesveika! Kitoks galėsi būti tik po 24 valandų ❌\n"
                f"Liko: {remaining}"
            )
            return

    media_file = random.choice(available_media)
    message_text = media_messages.get(media_file, "")

    file_path = os.path.join(media_folder, media_file)
    if os.path.exists(file_path):
        await ctx.send(content=message_text, file=discord.File(file_path))
    else:
        await ctx.send("❌ Failas nerastas! ❌")

    user_cooldowns[user_id] = now

@bot.command(name="sarasas")
async def sarasas(ctx):
    komandu_sarasas = (
        "**Komandų sąrašas:**\n"
        ".koks"
    )
    await ctx.send(komandu_sarasas)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        if ctx.invoked_with not in [c.name for c in bot.commands]:
            await ctx.send("❌ Tokios komandos nėra! ❌")
    else:
        print(f"Klaida komandoje {ctx.command}: {error}")

bot.run(TOKEN)