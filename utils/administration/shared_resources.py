"""
Shared resources for management-related components.
"""
from datetime import datetime
import asyncio
import os
import signal
import sys
from time import time
from discord.ext import commands
from pathlib import Path
import discord
import pytz

reboot_timestamp_dir = Path('.') / 'data'
reboot_timestamp_dir.mkdir(exist_ok=True)
reboot_timestamp_filename = 'reboot_time.txt'

def _update_reboot_timestamp(reboot_time = None):
    """
    Internal helper. Small function to update reboot time (writes to a
    temporary file). In the future, will consider migrating this functionality
    to a database-involved or JSON solution.
    """
    time_zone = pytz.timezone('US/Central')

    # if passed-in reboot time is type 'datetime.datetime'
    if isinstance(reboot_time, datetime):
        reboot_time = reboot_time.astimezone(tz=time_zone)
    # if passed-in reboot time is type 'time.time'
    elif isinstance(reboot_time, time):
        reboot_time = datetime.fromtimestamp(
            reboot_time).astimezone(time_zone)
    # if reboot time was not passed in, default to datetime.datetime.now()
    else:
        reboot_time = datetime.now(tz=time_zone)

    with (
        reboot_timestamp_dir / reboot_timestamp_filename
    ).open('w') as opened_file:
        # format the time, then write to file
        time_format = "%Y-%m-%d %H:%M:%S %Z%z"
        opened_file.write(reboot_time.strftime(time_format))


async def _reboot_bot(bot: discord.Bot):
    """
    Internal helper. Reboots bot by sending termination signal to OS.
    Requires proper setup of script running in systemd.
    """
    try:
        # create a temporary file with current timestamp;
        # this will be picked up by git_manager when bot restarts
        _update_reboot_timestamp()

        # NOTE:
        # signal.signal(signal.SIGQUIT, SIG_DFL) may not work on Windows!
        #
        # although, seems users may be saying this is a recent issue in the
        # pycord version 2.5.0;
        #
        # keeping this error for now to see if a fix for this issue
        # in pycord v2.5.0 will resolve the error
        await bot.close()

        # NOTE:
        # this code block *does* kill the bot, but relies on systemd service
        # configuration to ensure the restart of the <main.py> script for
        # this bot;
        # also, self.bot.close() by itself causes same console error as
        # including signal.signal(...) and os.kill(...);
        #
        # windows does not deal with "signals" like "SIGQUIT", so only do this
        # for linux (which is the intended OS for cloud hosting)
        if sys.platform.startswith('linux'):
            signal.signal(signal.SIGQUIT, signal.SIG_DFL)
            os.kill(os.getpid(), signal.SIGQUIT)

    except Exception as e:
        #raise commands.CommandError(
        #    f"[Management] Failed to manually reboot: {e}"
        #)
        print(f"[_reboot_bot] {repr(e)}", file=sys.stderr)


class YesNoView(discord.ui.View):
    """
    Button (sub)class for confirming yes or no.

    Sidenote: a set of buttons you want to be displayed together should be put in
    their own subclass. In this case, YesNoView is a subclass specifically to
    display yes/no buttons.

    Each button callback method needs to be uniquely named, e.g.,
    - async def button_callback1
    - async def button_callback2
    
    Button callbacks are distinguished by the @discord.ui.button(...)
    decorator, which you must put a label and/or custom_id to distinguish.
    """
    def __init__(self, *args, **kwargs):
        """
        Using explicit init here in case I need to modify or add attribute
        """
        super().__init__(*args, **kwargs)
        self.yes = False

    @discord.ui.button(
            label="Yes",
            custom_id="yes_button_1",
            style=discord.ButtonStyle.green
    )
    async def button_callback_yes(self, button, interaction):
        self.yes = True
        self.disable_all_items()
        await interaction.response.edit_message(content="Confirmed.")
        self.stop()
    
    @discord.ui.button(
        label="No",
        custom_id="no_button_1",
        style=discord.ButtonStyle.gray
    )
    async def button_callback_no(self, button, interaction):
        self.yes = False
        self.disable_all_items()
        await interaction.response.edit_message(content="Confirmed.")
        self.stop()
        
        