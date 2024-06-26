import os
from datetime import datetime
from time import time
from discord.ext import tasks, commands
from discord import option
from pathlib import Path
import discord
import git
import pytz
from utils.administration.shared_resources import (
    _reboot_bot,
    reboot_timestamp_dir,
    reboot_timestamp_filename,
    _update_reboot_timestamp
)

_update_interval = 300 #seconds

class GitManager(commands.Cog):
    """
    Git code management class/Cog. Focused on up-to-date code management.
    """

    # define slash (/) command prefix name to use in discord channels
    git_slash = discord.SlashCommandGroup("git", "git management")

    def __init__(self, bot):
        self.bot = bot
        self.git_auto_update.start()
        self.last_update = (self._read_reboot_time() or time())
        self.last_pull = None

        # using 'os.get_cwd()' assumes application doesn't change directory
        # after startup
        self.humble_repo = f"{os.getcwd()}"

        # used to determine if entire restart necessary for bot;
        # if a git pull results in updated code, then self._git_pull(...)
        # should update this field to True
        self.repo_has_changed_flag : bool = False

    def cog_unload(self):
        print("[GitManager][cog_unload] cog unload called!")
        self.git_auto_update.cancel()
        super().cog_unload()

    def _read_reboot_time(self):
        """
        Internal helper. If the file exists, read timestamp from reboot
        timestamp file (should be in 'shared_resources.py').
        """
        timestamp = None
        p = reboot_timestamp_dir / reboot_timestamp_filename

        if Path.exists(p):
            with (p).open('r') as reboot_timestamp:
                try:
                    # read the timestamp stored in the file,
                    # then assign timestamp to self.last_update
                    timestamp = reboot_timestamp.read_text()
                except:
                    pass

        # delete the timestamp file (may change in future), and return value
        p.unlink(missing_ok=True)
        return timestamp

    def repo_has_changed(self):
        """
        Internal helper method. Returns true if any of Humble Helper's code
        has changed.
        """
        repo_path = self.humble_repo

        repo = git.Repo(repo_path)
        current = repo.head.commit

        if current == repo.head.commit:
            print("[GitManager][repo_has_changed] No code changes found!")
            self.repo_has_changed_flag = False
        else:
            print(
                "[GitManager][repo_has_changed] "
                "Code updated! Restart required."
            )
            self.repo_has_changed_flag = True

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
            
            # update 'self.last_pull' timestamp
            self.last_pull = time()

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

        # don't perform git pull OR restart, if too early
        if time() - self.last_update < _update_interval:
            print(
                "[GitManager][_git_pull_and_restart] too early, not updating"
            )
            return

        # perform the git pull
        await self._git_pull()

        # only restart if code was updated after a git pull
        if self.repo_has_changed():
            await self._restart_bot()


    @tasks.loop(seconds=_update_interval)
    async def git_auto_update(self):
        """
        Automated method/task to update HumbleHelper code base.
        """
        print(
            f"[GitManager][git_auto_update()]: "
            f"Codebase update automatically triggered! "
            f"({round(_update_interval/60)}min)",  
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


    @git_slash.command(
        name="pullstats",
        #guild_ids=[]
        description="Get codebase stats on HumbleHelper"
    )
    @commands.has_guild_permissions(administrator=True)
    async def pull_stats(self, ctx):
        """
        Fetch codebase statistics on HumbleHelper
        """
        time_format = "%Y-%m-%d %H:%M:%S %Z%z"
        time_zone = pytz.timezone('US/Central')

        last_pull_cst = datetime.fromtimestamp((self.last_pull or 0))
        last_pull_cst = last_pull_cst.astimezone(
            time_zone).strftime(time_format)

        last_update_cst = datetime.fromtimestamp((self.last_update or 0))
        last_update_cst = last_update_cst.astimezone(
            time_zone).strftime(time_format)
        
        stats = (
            f"```"
            f"Last git pull was performed "
            f"on {last_pull_cst}.\n"
            f"Last reboot was performed "
            f"on {last_update_cst}.\n"
            f"Git pull update interval is: {round(_update_interval/60)} min."
            f"```"
        )
        await ctx.respond(stats)


# register GitManager cog to the bot
def setup(bot):
    bot.add_cog(GitManager(bot))