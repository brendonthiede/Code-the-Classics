# [Choice] Python version: 3.12-bookworm, 3.11-bookworm, 3.10-bookworm
ARG VARIANT=3.12-bookworm
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# pygbag bundles its own copy of emscripten/SDL2 for WASM compilation, so we
# only need Python and pip here – no X11/VNC/audio stack required.
COPY requirements.txt /tmp/pip-tmp/
RUN pip install --upgrade pip \
    && pip install -r /tmp/pip-tmp/requirements.txt \
    && pip install pygbag \
    && rm -rf /tmp/pip-tmp
