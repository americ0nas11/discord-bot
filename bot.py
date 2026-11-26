import os
import discord
import random
from datetime import datetime, timedelta
from discord.ext import commands
from discord import Activity, ActivityType

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", ".")

if not TOKEN:
    raise ValueError("❌ DISCORD_TOKEN nerastas!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

user_cooldowns = {}


media_cooldowns = {}          
MEDIA_COOLDOWN = timedelta(hours=24)

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
    "35.png": "Šiandien tu ohota i rybalka LUKAS 🐟",
    "36.png": "Šiandien tu aciputes, nes i tave ziuri mergytes ARNAS 🎤",
    "37.png": "Šiandien tu pisi siurpo karaoke JOKŪBS 🎤",
    "38.png": "Šiandien tu strategiskai patogioje vietoje su nekilnojamo turto agentu Joriu 😎",
    "39.png": "Šiandien tu katik nuo kalno nukrites mariukas 🩸",
    "40.png": "Šiandien tu sokes ant baltu mariukas 😠",
    "41.png": "Šiandien tu pozuojantis po gero baliaus mariukas 😊",
    "42.png": "Šiandien tu is po kariuomenes lengvai pakrites ant ruliu vitas 🪖",
    "43.png": "Šiandien tu mumija kraliku bosas 👻",
    "44.png": "Šiandien tu rodai savo alkoholiko sugebejimus marka 🍺",
    "45.png": "Šiandien tu visiskai pakrites ir tau ragas marka 🙇",
}

available_media = list(media_messages.keys())


def format_remaining(delta: timedelta) -> str:
    """Suformatuoja timedelta į gražų 'Xh Ym Zs' tekstą, be mikrosekundžių."""
    total_seconds = int(delta.total_seconds())
    if total_seconds < 0:
        total_seconds = 0

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours} val. {minutes} min."
    elif minutes > 0:
        return f"{minutes} min. {seconds} sek."
    else:
        return f"{seconds} sek."


def get_available_media(now: datetime):
    """Grąžina sąrašą nuotraukų, kurios NĖRA 12h cooldown'e."""
    return [
        m for m in available_media
        if m not in media_cooldowns or (now - media_cooldowns[m]) >= MEDIA_COOLDOWN
    ]


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
        cooldown = timedelta(hours=12)

        if passed < cooldown:
            remaining = cooldown - passed
            await ctx.send(
                f"❌ Kas per daug tas nesveika! Kitoks galėsi būti tik po 12 valandų ❌\n"
                f"Liko: {format_remaining(remaining)}"
            )
            return


    choices = get_available_media(now)

    if not choices:

        soonest = min(available_media, key=lambda m: media_cooldowns.get(m, datetime.min))
        remaining = MEDIA_COOLDOWN - (now - media_cooldowns[soonest])
        await ctx.send(
            f"❌ Šiuo metu visos nuotraukos ilsisi! Bandyk vėliau ❌\n"
            f"Artimiausia atsilaisvins po: {format_remaining(remaining)}"
        )
        return

    media_file = random.choice(choices)
    message_text = media_messages.get(media_file, "")

    file_path = os.path.join(media_folder, media_file)
    if os.path.exists(file_path):
        await ctx.send(content=message_text, file=discord.File(file_path))
    else:
        await ctx.send("❌ Failas nerastas! ❌")

    user_cooldowns[user_id] = now
    media_cooldowns[media_file] = now

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

try:
    bot.run(TOKEN)
except Exception as e:
    import sys
    print(f"KLAIDA: {e}", flush=True)
    sys.stdout.flush()