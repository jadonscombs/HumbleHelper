#!/bin/bash
# [shell quick compose deployment script on linux]
# NOTE:
#   this script should be executed on your local workstation, to
#   actually build and deploy the docker containers
#
# NOTE:
#   this script is NOT to be run in an already running docker container!

# check if .env file exists in project root and size greater than 0 bytes
if [[ ! -s ./.env]]; then
    echo """Please create an '.env' file here, and insert the following text: 
    BOT_TOKEN=<your.discord.bot.token>"""
    exit 1
fi

# test if .env file's "BOT_TOKEN" field is non-empty/non-null before evaluating
source .env
if [[ ! -z "${BOT_TOKEN}" ]]; then
    echo """Please create an '.env' file here, and insert the following text: 
    BOT_TOKEN=<your.discord.bot.token>"""
    exit 1
fi

# execute helper bot deployment with "docker compose" command
docker compose up -d --build