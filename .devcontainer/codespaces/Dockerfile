# [Choice] Python version: 3.12-bookworm, 3.11-bookworm, 3.10-bookworm
ARG VARIANT=3.12-bookworm
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# Virtual display stack (Xvfb + VNC + noVNC) and SDL/audio dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    openbox \
    pulseaudio \
    libpulse0 \
    libasound2-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev

COPY requirements.txt /tmp/pip-tmp/
RUN pip install --upgrade pip && pip install -r /tmp/pip-tmp/requirements.txt && rm -rf /tmp/pip-tmp

COPY .devcontainer/codespaces/start-display.sh /usr/local/bin/start-display.sh
RUN chmod +x /usr/local/bin/start-display.sh
