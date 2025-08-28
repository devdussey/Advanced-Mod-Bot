import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import action_embed, info_embed
from utils.database import add_warning, get_warnings
import asyncio


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # -----------------------------
    # Ban command
    # -----------------------------
    @app_commands.command(name="ban",
                          description="Ban a user (requires a reason).")
    async def ban(self, interaction: discord.Interaction, user: discord.Member,
                  reason: str):
        await user.ban(reason=reason)
        embed = action_embed("🚨 User Banned", user, interaction.user, reason)
        await interaction.response.send_message(embed=embed)

    # -----------------------------
    # Kick command
    # -----------------------------
    @app_commands.command(name="kick",
                          description="Kick a user (requires a reason).")
    async def kick(self, interaction: discord.Interaction,
                   user: discord.Member, reason: str):
        await user.kick(reason=reason)
        embed = action_embed("👢 User Kicked", user, interaction.user, reason,
                             discord.Color.orange())
        await interaction.response.send_message(embed=embed)

    # -----------------------------
    # Mute command
    # -----------------------------
    @app_commands.command(
        name="mute", description="Timeout a user for a set number of minutes.")
    async def mute(self, interaction: discord.Interaction,
                   user: discord.Member, minutes: int, reason: str):
        duration = discord.utils.utcnow() + discord.timedelta(minutes=minutes)
        await user.timeout(until=duration, reason=reason)
        embed = action_embed("🔇 User Muted", user, interaction.user,
                             f"{reason} (for {minutes} min)")
        await interaction.response.send_message(embed=embed)

    # -----------------------------
    # Warn command
    # -----------------------------
    @app_commands.command(name="warn",
                          description="Warn a user (requires a reason).")
    async def warn(self, interaction: discord.Interaction,
                   user: discord.Member, reason: str):
        await add_warning(user.id, interaction.user.id, reason)
        embed = action_embed("⚠️ User Warned", user, interaction.user, reason,
                             discord.Color.yellow())
        await interaction.response.send_message(embed=embed)

    # -----------------------------
    # View warnings
    # -----------------------------
    @app_commands.command(name="warnings",
                          description="Check a user's warnings.")
    async def warnings(self, interaction: discord.Interaction,
                       user: discord.Member):
        rows = await get_warnings(user.id)
        if not rows:
            await interaction.response.send_message(embed=info_embed(
                "No Warnings", f"{user.mention} has no warnings."))
            return

        embed = discord.Embed(title=f"⚠️ Warnings for {user}",
                              color=discord.Color.yellow())
        for i, row in enumerate(rows, start=1):
            embed.add_field(
                name=f"Warning {i}",
                value=
                f"Moderator: <@{row[2]}>\nReason: {row[3]}\nDate: {row[4]}",
                inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
