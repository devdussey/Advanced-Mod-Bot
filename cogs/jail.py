import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import action_embed, info_embed
from utils.database import jail_user, get_jailed_user, unjail_user, set_setting, get_setting
import json


class Jail(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # -----------------------------
    # Set jail role
    # -----------------------------
    @app_commands.command(
        name="setjailrole",
        description="Set the role to be used as the jail role.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setjailrole(self, interaction: discord.Interaction,
                          role: discord.Role):
        await set_setting("jail_role_id", str(role.id))
        await interaction.response.send_message(embed=info_embed(
            "✅ Jail Role Set",
            f"{role.mention} will now be used as the jail role."),
                                                ephemeral=True)

    # -----------------------------
    # Jail user
    # -----------------------------
    @app_commands.command(
        name="jail", description="Send a user to jail (requires a reason).")
    async def jail(self, interaction: discord.Interaction,
                   user: discord.Member, reason: str):
        jail_role_id = await get_setting("jail_role_id")
        if not jail_role_id:
            await interaction.response.send_message(embed=info_embed(
                "⚠️ Error", "Jail role not set! Use `/setjailrole`."),
                                                    ephemeral=True)
            return

        jail_role = interaction.guild.get_role(int(jail_role_id))
        if not jail_role:
            await interaction.response.send_message(embed=info_embed(
                "⚠️ Error", "Jail role not found in this server."),
                                                    ephemeral=True)
            return

        # Save original roles
        original_roles = [
            r.id for r in user.roles if r != interaction.guild.default_role
        ]
        await jail_user(user.id, original_roles, interaction.user.id, reason)

        # Remove roles & add jail role
        await user.edit(roles=[jail_role], reason=reason)

        embed = action_embed("🚔 User Jailed", user, interaction.user, reason)
        await interaction.response.send_message(embed=embed)

    # -----------------------------
    # Unjail user
    # -----------------------------
    @app_commands.command(name="unjail",
                          description="Release a user from jail.")
    async def unjail(self, interaction: discord.Interaction,
                     user: discord.Member):
        jailed = await get_jailed_user(user.id)
        if not jailed:
            await interaction.response.send_message(embed=info_embed(
                "⚠️ Error", f"{user.mention} is not jailed."),
                                                    ephemeral=True)
            return

        # Restore roles
        original_roles = json.loads(jailed[2])  # roles_json
        roles = [
            interaction.guild.get_role(rid) for rid in original_roles
            if interaction.guild.get_role(rid)
        ]
        await user.edit(roles=roles, reason="Unjailed")

        await unjail_user(user.id)

        embed = action_embed("✅ User Unjailed",
                             user,
                             interaction.user,
                             "Released from jail",
                             color=discord.Color.green())
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Jail(bot))
