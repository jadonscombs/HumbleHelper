import os
from discord.ext import tasks, commands
from discord import option
import discord
import git


class GitManager(commands.Cog):
    """
    Git code management class/Cog. Focused on up-to-date code management.
    """
    
    # define slash (/) command prefix name to use in discord channels
    git_slash = discord.SlashCommandGroup("git", "git management")

    def __init__(self, bot):
        self.bot = bot

        # using 'os.get_cwd()' assumes application doesn't change directory
        # after startup
        self.humble_repo = f"{os.getcwd()}"


    async def _git_pull(self):
        """
        Internal helper method. Execute a git pull on Humble Helper's repo
        to update its current code base
        """

        print("[GitManager][_git_pull]: git pull executing...")

        # repo = git.Repo(self.humble_repo)
        # origin = repo.remote(name='origin')
        # origin.pull()

        print("[GitManager][_git_pull]: finished git pull")


    async def _restart_bot(self):
        """
        Small helper. Simply restarts bot (uses internal shell script).
        """
        print("[GitManager][_restart_bot]: restarting HumbleHelper now!")
        # subprocess.run("path/to/restart_script.sh")


    async def _git_pull_and_restart(self):
        """
        Small helper. Executes a git pull AND restarts the bot
        """
        print("[GitManager][_git_pull_and_restart]: ...")
        await self._git_pull()
        await self._restart_bot()


    #@tasks.loop(hours=1)
    @tasks.loop(minutes=1)
    async def git_auto_update(self):
        """
        Automated method/task to update HumbleHelper code base.
        """
        await ctx.respond(
            "[GitManager][git_auto_update()]: "
            "Codebase update automatically triggered! (1min)",
            ephemeral=True
        )
        await self._git_pull_and_restart()


    @commands.slash_command(
        name="git_pull",
        #guild_ids=[],
        description="Manually trigger HumbleHelper code update."
    )
    @commands.has_guild_permissions(administrator=True)
    async def force_git_pull(self, ctx):
        """
        Manually trigger HumbleHelper code update.
        """
        await ctx.respond(
            "[force_git_pull()]: Codebase update manually triggered!",
            ephemeral=True
        )
        await self._git_pull_and_restart()


# register GitManager cog to the bot
def setup(bot):
    bot.add_cog(GitManager(bot))