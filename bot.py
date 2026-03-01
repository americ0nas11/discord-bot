import os
import discord
from discord.ext import commands

# 🔹 Gaunam token ir prefix tiesiog iš environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", ".")

if not TOKEN:
    raise ValueError("❌ DISCORD_TOKEN nerastas! Nustatyk jį kaip environment variable")

# 🔹 Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# 🔹 Pavyzdinė komandaa
@bot.command(name="komandos")
async def komandos(ctx):
    await ctx.send("Komandų sąrašas: .koks")

# 🔹 Start bot
bot.run(TOKEN)