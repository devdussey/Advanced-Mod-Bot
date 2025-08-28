import discord
from discord.ext import commands
import asyncio
import os

from utils.database import init_db

# Get secrets from environment (Replit Secrets Manager)
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load all cogs
async def load_cogs():
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.jail")
    await bot.load_extension("cogs.autorole")
    await bot.load_extension("cogs.logging")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print("✅ Slash commands synced.")
    except Exception as e:
        print(f"⚠️ Failed to sync commands: {e}")

async def main():
    async with bot:
        await init_db()
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
