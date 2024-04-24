"""
Initializer file for HumbleHelper application. Contains startup environment
essentials.
"""

import configparser
import os
import sys
from pathlib import Path


def fetch_initialization_data() -> str:
    """
    Internal helper. Return initialization data required for bot startup.
    """
    try:
        # read in initialization data
        config = configparser.ConfigParser()
        config.read(Path("./data/bot_config.ini"))

        # only proceed if config file has an "AUTH" section
        if "AUTH" in config.sections():
            
            if "tkn" in config.options("AUTH"):
                return config["AUTH"]["tkn"]
                
            # this code is only ever reached if an error occurs    
            print(
                "[fetch_initialization_data()] "
                "Malformed initialization data. Exiting...",
                file=sys.stderr
            )
            sys.exit(1)
    except:
        sys.exit(1)


def fetch_all_cogs(cog_dirs: tuple = None) -> list | None:
    """
    Internal helper function. Return a list of cogs to load into bot.
    """

    # provide static list of cog file locations if not externally passed in
    if cog_dirs is None:
        cog_dirs = (
            "./cogs/",
            "./utils/administration/"
        )
    cog_list = []

    # iterate over every cog directory specified;
    # adds extension names for HumbleHelper bot to attempt to load
    for dir in cog_dirs:

        # if a directory pydoesn't exist, create it
        p = Path(dir)
        os.makedirs(p, exist_ok=True)

        try:
            # remove leading "./" and trailing "/";
            # replace remaining "/" with "."
            cog_prefix = dir.rstrip("/").lstrip("./").replace("/", ".")

            # iterate over each file in the current directory
            for filename in os.listdir(dir):
                if not filename.endswith(".py"):
                    continue
                cog_list += [
                    f"{cog_prefix}.{filename[:-3]}"
                ]

        except Exception as err:
            print(repr(err), file=sys.stderr)

    cog_list_str = '\n'.join(cog_list)
    print(f"returning cog list:\n{cog_list_str}")
    return cog_list