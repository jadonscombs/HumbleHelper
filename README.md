# HumbleHelper
Productivity application. Get more done, save that backlog of ideas, and more!
Made with love (and [PyCord](https://docs.pycord.dev/en/stable/))

Currently, I have this running privately, configured as a persistent service using `systemd`.

## Features Included
- Automated and manual codebase updating
- Automated and manual application reboot (w/safety features)
- Simplified code architecture (easily identify components)
- Manual reload of application components ("Cogs")

## Planned Features
- Reminder and TODO-list management (empower yourself to conquer every day/week/month!)
- Backlog text and ideas management (so you don't lose that passing thought!)

## Quick Start (Rough Instructions)
1. Pre-requisites:
  - You have installed Python 3.10 or above on your target system
  - You have your own discord bot created (go to [Discord Developer Portal](https://discord.com/developers)), bot invite permissions configured, and access to its OAuth token
  - You understand these instructions will *only* describe how to run the bot manually (e.g., *not* as a service)

1. Clone this repo in desired destination
2. Create a Python 3.10 virtual environment (I usually call it `.venv`) within the repo
3. Activate the virtualenv
   - **Ubuntu or Linux OS:** Run `source {project folder}/{your_venv}/bin/activate`
   - **Windows:** Run `{project folder}\{your_venv}\Scripts\activate.bat`
4. Once virtual environment activated, install all depedencies for project
   - Run `pip install -r requirements.txt`
5. Set your own bot token
   1. Create a `data` folder in project folder, for example: `{project root}/data/`
   2. Create a `bot_config.ini` file in the `data` folder: `{project root}/data/bot_config.ini`
   3. Type the following inside `bot_config.ini` and **save**:
      ```
      [AUTH]
      tkn = {YOUR.REALLY_LONG.BOT_TOKEN}
      ```
6. Now you can run the bot application: `python main.py`

## Lastly...
If you have encountered any issues while running this application, please let me know and I will be sure to resolve it for you. Thanks!
