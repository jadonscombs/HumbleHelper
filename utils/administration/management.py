from discord.ext import tasks, commands
from discord import option
import discord


class Management(commands.Cog):
    """
    Generalized management class/Cog. Focused on generalized bot management.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="reload",
        description="Reload a currently loaded Cog/extension"
    )
    @commands.has_guild_permissions(administrator=True)
    async def reload_extension(self, ctx, extension: str):
        self.bot.reload_extension(extension)
        await ctx.respond(f'Cog {extension} reloaded.', ephemeral=True)


# register Management cog to the bot
def setup(bot):
    bot.add_cog(Management(bot))