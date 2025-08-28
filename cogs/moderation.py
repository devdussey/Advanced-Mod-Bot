import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import action_embed, info_embed
from utils.database import add_warning, get_warnings, clear_warnings
from datetime import timedelta


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # -----------------------------
    # Ban command
    # -----------------------------
    @app_commands.command(name="ban",
                          description="Ban a user (requires a reason).")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member,
                  reason: str):
        await user.ban(reason=reason)
        embed = action_embed("🚨 User Banned", user, interaction.user, reason)
        await interaction.response.send_message(embed=embed)

    # -----------------------------
    # Unban command
    # -----------------------------
    @app_commands.command(
        name="unban", description="Unban a user by ID (requires a reason).")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str,
                    reason: str):
        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user, reason=reason)
        embed = action_embed("✅ User Unbanned", user, interaction.user, reason,
                             discord.Color.green())
        await interaction.response.send_message(embed=embed)

    # -----------------------------
    # Kick command
    # -----------------------------
    @app_commands.command(name="kick",
                          description="Kick a user (requires a reason).")
    @app_commands.checks.has_permissions(kick_members=True)
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
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction,
                   user: discord.Member, minutes: int, reason: str):
        until = discord.utils.utcnow() + timedelta(minutes=minutes)
        await user.timeout(until=until, reason=reason)
        embed = action_embed("🔇 User Muted", user, interaction.user,
                             f"{reason} (for {minutes} min)")
        await interaction.response.send_message(embed=embed)

    # -----------------------------
    # Unmute command
    # -----------------------------
    @app_commands.command(
        name="unmute",
        description="Remove timeout from a user (requires a reason).")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction,
                     user: discord.Member, reason: str):
        await user.timeout(until=None, reason=reason)
        embed = action_embed("✅ User Unmuted", user, interaction.user, reason,
                             discord.Color.green())
        await interaction.response.send_message(embed=embed)

    # -----------------------------
    # Warn command
    # -----------------------------
    @app_commands.command(name="warn",
                          description="Warn a user (requires a reason).")
    @app_commands.checks.has_permissions(moderate_members=True)
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
    @app_commands.checks.has_permissions(moderate_members=True)
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

    # -----------------------------
    # Clear warnings
    # -----------------------------
    @app_commands.command(name="clearwarnings",
                          description="Clear all warnings for a user.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def clearwarnings(self, interaction: discord.Interaction,
                            user: discord.Member):
        await clear_warnings(user.id)
        await interaction.response.send_message(embed=info_embed(
            "✅ Warnings Cleared",
            f"All warnings for {user.mention} have been cleared."),
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
