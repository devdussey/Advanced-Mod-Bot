import discord
from discord.ext import commands
from discord import app_commands
from utils.database import set_setting, get_setting
from utils.embeds import info_embed


class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # -----------------------------
    # Set log channel
    # -----------------------------
    @app_commands.command(name="setlogchannel",
                          description="Set the channel for moderation logs.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setlogchannel(self, interaction: discord.Interaction,
                            channel: discord.TextChannel):
        await set_setting("log_channel_id", str(channel.id))
        await interaction.response.send_message(embed=info_embed(
            "✅ Log Channel Set", f"Logs will be sent to {channel.mention}."),
                                                ephemeral=True)

    # -----------------------------
    # Listener for moderation actions
    # -----------------------------
    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction,
                                        command: app_commands.Command):
        """
        Fires when a slash command completes. 
        Sends the response embed (if present) to the log channel.
        """
        log_channel_id = await get_setting("log_channel_id")
        if not log_channel_id:
            return

        log_channel = interaction.guild.get_channel(int(log_channel_id))
        if not log_channel:
            return

        try:
            if interaction.response.is_done():
                # Fetch recent messages in the channel to find bot's embed
                history = [
                    msg async for msg in interaction.channel.history(limit=5)
                ]
                for msg in history:
                    if msg.author == self.bot.user and msg.embeds:
                        await log_channel.send(embed=msg.embeds[0])
                        break
        except Exception as e:
            print(f"⚠️ Logging error: {e}")


async def setup(bot):
    await bot.add_cog(Logging(bot))