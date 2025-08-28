import asyncio
import os

import discord
from discord.ext import commands

from utils.database import init_db

# Get secrets from Replit's secrets manager (environment variables)
TOKEN = os.getenv("DISCORD_TOKEN")
guild_id_str = os.getenv("GUILD_ID")
if guild_id_str is None:
    raise ValueError("GUILD_ID environment variable not set.")
GUILD_ID = int(guild_id_str)  # Replace with your server ID in secrets

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)


# Load cogs
async def load_cogs():
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.jail")
    await bot.load_extension("cogs.autorole")
    await bot.load_extension("cogs.logging")


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

    # Sync slash commands to a specific guild
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print("✅ Slash commands synced.")
    except Exception as e:
        print(f"⚠️ Failed to sync commands: {e}")


# Run bot
async def main():
    async with bot:
        await init_db()  # Initialize SQLite tables
        await load_cogs()
        await bot.start(TOKEN)


asyncio.run(main())
