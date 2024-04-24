"""
Driver script for Discord HumbleHelper application.

SUBJECT TO LICENSE ATTACHED TO THIS REPO.
"""

import sys
import discord
from discord import option
from discord.ext import commands
from utils.initialize import fetch_initialization_data as fetch_auth
from utils.initialize import fetch_all_cogs


# necessary additions for Discord bot
intents = discord.Intents.all()
intents.message_content = True
bot = discord.Bot(intents=intents)


def load_cogs(bot: discord.Bot):
    """
    Internal helper. Load all found cogs into bot.
    """

    # load all detected cogs/"feature extensions" into bot
    cog_list = fetch_all_cogs()
    for cog in cog_list:
        try:
            bot.load_extension(cog)
        except (discord.ExtensionNotFound, discord.NoEntryPointError) as err:
            #print(repr(err), file=sys.stderr)
            continue
        except Exception as err:
            print(repr(err), file=sys.stderr)

@bot.event
async def on_ready():
    print(f'Initialized. Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # ignore this bot's own messages
    if message.author == bot.user:
        return


if __name__ == "__main__":
    load_cogs(bot)


bot.run(fetch_auth())