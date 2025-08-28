import discord
from datetime import datetime


def action_embed(title: str,
                 user: discord.Member,
                 moderator: discord.Member,
                 reason: str,
                 color=discord.Color.red()):
    """
    Creates a neat embed for moderation actions.
    """
    embed = discord.Embed(title=title,
                          color=color,
                          timestamp=datetime.utcnow())
    embed.add_field(name="👤 User",
                    value=f"{user.mention} ({user.id})",
                    inline=False)
    embed.add_field(name="🛡️ Moderator",
                    value=f"{moderator.mention} ({moderator.id})",
                    inline=False)
    embed.add_field(name="📝 Reason", value=reason, inline=False)
    return embed


def info_embed(title: str, description: str, color=discord.Color.blue()):
    """
    Creates a general info embed (for things like /unjail confirmation, autorole info, etc.).
    """
    embed = discord.Embed(title=title,
                          description=description,
                          color=color,
                          timestamp=datetime.utcnow())
    return embed
