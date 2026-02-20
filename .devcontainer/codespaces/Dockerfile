FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

COPY requirements.txt /tmp/pip-tmp/
RUN pip install -r /tmp/pip-tmp/requirements.txt && rm -rf /tmp/pip-tmp

RUN apt-get update && apt-get install -y libpulse0 libasound2 libasound2t64 libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
