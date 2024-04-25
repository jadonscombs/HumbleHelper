"""
Shared resources for management-related components.
"""
from datetime import datetime
import asyncio
import os
import signal
import sys
from discord.ext import commands
from pathlib import Path
import discord
import pytz

reboot_timestamp_dir = Path('.') / 'data'
reboot_timestamp_dir.mkdir(exist_ok=True)
reboot_timestamp_filename = 'reboot_time.txt'

async def _reboot_bot(bot: discord.Bot):
    """
    Internal helper. Reboots bot by sending termination signal to OS.
    Requires proper setup of script running in systemd.
    """
    try:
        # create a temporary file with current timestamp;
        # this will be picked up by git_manager when bot restarts
        reboot_time = datetime.now(
            format="%Y-%m-%d %H:%M:%S %Z%z",
            tz=pytz.timezone('US/Central')
        )

        with (
            reboot_timestamp_dir / 'reboot_time.txt'
        ).open('w') as opened_file:
            opened_file.write(reboot_time)

        # NOTE:
        # this code block *does* kill the bot, but relies on systemd service
        # configuration to ensure the restart of the <main.py> script for
        # this bot;
        # also, self.bot.close() by itself causes same console error as
        # including signal.signal(...) and os.kill(...);
        #
        # NOTE:
        # signal.signal(signal.SIGQUIT, SIG_DFL) may not work on Windows!
        #
        # although, seems users may be saying this is a recent issue in the
        # pycord version 2.5.0;
        #
        # keeping this error for now to see if a fix for this issue
        # in pycord v2.5.0 will resolve the error
        await bot.close()

        # windows does not deal with "signals" like "SIGQUIT", so only do this
        # for linux (which is the intended OS for cloud hosting)
        if sys.platform.startswith('linux'):
            signal.signal(signal.SIGQUIT, signal.SIG_DFL)
            os.kill(os.getpid(), signal.SIGQUIT)

    except Exception as e:
        #raise commands.CommandError(f"[Management] Failed to manually reboot: {e}")
        print(repr(e), file=sys.stderr)


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
        
        