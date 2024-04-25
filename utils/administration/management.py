from discord.ext import commands
from discord import option
from utils.administration.shared_resources import YesNoView, _reboot_bot

class Management(commands.Cog):
    """
    Generalized management class/Cog. Focused on generalized bot management.
    """

    def __init__(self, bot):
        self.bot = bot

    async def _reboot_bot(self):
        """
        Internal helper. Reboots bot.

        Created container method for reboot, in case other tasks need to be
        performed before the _reboot_bot(...) call.
        """
        await _reboot_bot(self.bot)

    async def do_reboot(self, ctx):
        """
        Helper for the 'reboot' command. Consolidates two actions:
        1. await ctx.respond(...)
        2. perform the reboot
        """
        await ctx.respond("Rebooting now...", ephemeral=True)
        try:
            await self._reboot_bot()
        except Exception as e:
            await ctx.send(f"[Management] Reboot failed: {repr(e)}")

    @commands.slash_command(
        name="reboot",
        description="Reboot the bot. Requires script to run in systemd."
    )
    @option(
        "force",
        description="(Optional) Force reboot. Use 'yes','y', or 'true'",
        required=False,
        default="false"
    )
    @commands.has_guild_permissions(administrator=True)
    async def reboot(self, ctx, force: str):
        """
        Note: there are 'return' statements, however 
        """
        if force.lower() in ("true", "yes", "y"):
            await self.do_reboot(ctx)
            return

        # wait <timeout> seconds for user to press "yes" or "no"
        view = YesNoView(timeout=10)
        await ctx.respond(
            "Would you like to reboot?",
            view=view,
            ephemeral=True
        )
        result = await view.wait()

        if view.yes:
            await self.do_reboot(ctx)
        else:
            await ctx.respond("Cancelling reboot.", ephemeral=True)

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