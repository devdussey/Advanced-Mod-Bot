import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import info_embed
from utils.database import set_setting, get_setting
import json


class Autorole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # -----------------------------
    # Set autorole
    # -----------------------------
    @app_commands.command(
        name="setautorole",
        description="Set a role to be given automatically on join.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setautorole(self, interaction: discord.Interaction,
                          role: discord.Role):
        current = await get_setting("autoroles")
        if current:
            roles = json.loads(current)
        else:
            roles = []

        if role.id not in roles:
            roles.append(role.id)

        await set_setting("autoroles", json.dumps(roles))
        await interaction.response.send_message(embed=info_embed(
            "✅ Autorole Added",
            f"{role.mention} will now be assigned on join."),
                                                ephemeral=True)

    # -----------------------------
    # Clear autoroles
    # -----------------------------
    @app_commands.command(name="clearautoroles",
                          description="Clear all autoroles.")
    @app_commands.checks.has_permissions(administrator=True)
    async def clearautoroles(self, interaction: discord.Interaction):
        await set_setting("autoroles", json.dumps([]))
        await interaction.response.send_message(embed=info_embed(
            "✅ Autoroles Cleared", "No roles will be assigned on join."),
                                                ephemeral=True)

    # -----------------------------
    # Event: Member join
    # -----------------------------
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        roles_json = await get_setting("autoroles")
        if not roles_json:
            return

        role_ids = json.loads(roles_json)
        roles = [
            member.guild.get_role(rid) for rid in role_ids
            if member.guild.get_role(rid)
        ]
        if roles:
            try:
                await member.add_roles(*roles, reason="Autorole system")
            except discord.Forbidden:
                print("⚠️ Missing permissions to assign autoroles.")


async def setup(bot):
    await bot.add_cog(Autorole(bot))
