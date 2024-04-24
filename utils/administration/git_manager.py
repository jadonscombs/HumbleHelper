import os
from time import time
from discord.ext import tasks, commands
from discord import option
import discord
import git
from utils.administration.shared_resources import _reboot_bot

update_interval = 300 #seconds

class GitManager(commands.Cog):
    """
    Git code management class/Cog. Focused on up-to-date code management.
    """
    
    # define slash (/) command prefix name to use in discord channels
    git_slash = discord.SlashCommandGroup("git", "git management")

    def __init__(self, bot):
        self.bot = bot
        self.git_auto_update.start()
        self.last_update = time()

        # using 'os.get_cwd()' assumes application doesn't change directory
        # after startup
        self.humble_repo = f"{os.getcwd()}"

    def cog_unload(self):
        print("[GitManager][cog_unload] cog unload called!")
        self.git_auto_update.cancel()
        super().cog_unload()

    async def close(self):
        self.cog_unload()

    async def _git_pull(self):
        """
        Internal helper method. Execute a git pull on Humble Helper's repo
        to update its current code base
        """

        print("[GitManager][_git_pull]: git pull executing...")
        try:
            repo = git.Repo(self.humble_repo)
            origin = repo.remote(name='origin')
            res = origin.pull(verbose=True)
            #print(f"functions of pull[0]: {dir(res[0])}")
            #print(f"contents of pull[0]: {res[0]}")

        except Exception as e:
            print(f"[GitManager][_git_pull]: ERROR:\n{repr(e)}")
            return

        print("[GitManager][_git_pull]: finished git pull")

    async def _restart_bot(self):
        """
        Small helper. Simply restarts bot (uses systemd).
        """
        print("[GitManager][_restart_bot]: restarting HumbleHelper now!")
        await _reboot_bot(self.bot)

    async def _git_pull_and_restart(self):
        """
        Small helper. Executes a git pull AND restarts the bot
        """
        print("[GitManager][_git_pull_and_restart]: ...", end='')

        # don't update if too early
        if time() - self.last_update < update_interval:
            print("too early, not updating")
            return
        
        # 
        print()
        await self._git_pull()
        await self._restart_bot()
        self.last_update = time()


    #@tasks.loop(hours=1)
    @tasks.loop(seconds=update_interval)
    async def git_auto_update(self):
        """
        Automated method/task to update HumbleHelper code base.
        """
        print(
            "[GitManager][git_auto_update()]: "
            "Codebase update automatically triggered! (1min)",  
        )
        await self._git_pull_and_restart()


    @git_slash.command(
        name="pull",
        #guild_ids=[],
        description="Manually trigger HumbleHelper code update."
    )
    @commands.has_guild_permissions(administrator=True)
    async def force_git_pull(self, ctx):
        """
        Manually trigger HumbleHelper code update.
        """
        await ctx.respond(
            "[force_git_pull]: Codebase update manually triggered!",
            ephemeral=True
        )
        await self._git_pull()
        #await self._git_pull_and_restart()


# register GitManager cog to the bot
def setup(bot):
    bot.add_cog(GitManager(bot))