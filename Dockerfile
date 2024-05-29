# NOTE:
# use this dockerfile for quick proof-of-concept deployment of the python bot.
# this deployment file by itself will NOT save any data stored during usage.
# 
# if you intend on persistent usage of the bot, please
# deploy with "compose.yml" instead (and DO NOT delete this file)

# using base python image (python >= 3.10)
FROM python:3.10.14-bookworm

# copy just "requirements.txt" to /app/ for dependency installation
#COPY requirements.txt /app/

# setting root working directory;
# this is "/humble_helper_root/" but any source directory can technically work
RUN mkdir -p /humble_helper_root
WORKDIR /humble_helper_root

# copy this project's relevant contents into the container at ${WORKDIR}
COPY ./ .
RUN rm quickstart.ps1 quickstart.sh
RUN echo "present working directory: $(pwd)"
RUN echo "$(ls)"

# install python dependencies from requirements.txt
RUN pip install -r requirements.txt

# set custom user-specific bot token
RUN mkdir -p /humble_helper_root/data/
WORKDIR /humble_helper_root/data
ARG BOT_TOKEN
RUN printf "[AUTH]\ntkn = " >> bot_config.ini
RUN printf $BOT_TOKEN >> bot_config.ini

WORKDIR /humble_helper_root

# run the bot now
CMD ["python3", "main.py"]



