#!/bin/bash
# Starts the virtual display stack required to run pygame/pgzero apps in Codespaces.
# Called via postStartCommand; all services are backgrounded so the script exits promptly.

DISPLAY_NUM=1
DISPLAY=":${DISPLAY_NUM}"
SCREEN_RESOLUTION="1280x720x24"
VNC_PORT=5901
NOVNC_PORT=6080

# --- Xvfb (virtual framebuffer) ---
if ! pgrep -x Xvfb > /dev/null; then
    Xvfb "${DISPLAY}" -screen 0 "${SCREEN_RESOLUTION}" &
    # Wait briefly for the display to come up
    sleep 1
    echo "Xvfb started on ${DISPLAY}"
else
    echo "Xvfb already running"
fi

export DISPLAY

# --- Openbox (lightweight window manager for proper window decorations) ---
if ! pgrep -x openbox > /dev/null; then
    DISPLAY="${DISPLAY}" openbox &
    echo "Openbox started"
fi

# --- PulseAudio with a null sink (enables game audio without real hardware) ---
if ! pgrep -x pulseaudio > /dev/null; then
    pulseaudio --start \
        --load="module-null-sink sink_name=game_audio" \
        --load="module-native-protocol-unix" \
        --exit-idle-time=-1 2>/dev/null || true
    echo "PulseAudio started with null sink"
fi

# --- x11vnc (VNC server on top of Xvfb) ---
if ! pgrep -x x11vnc > /dev/null; then
    x11vnc \
        -display "${DISPLAY}" \
        -rfbport "${VNC_PORT}" \
        -nopw \
        -listen localhost \
        -xkb \
        -ncache 10 \
        -ncache_cr \
        -forever \
        -quiet &
    sleep 1
    echo "x11vnc started on port ${VNC_PORT}"
fi

# --- noVNC / websockify (browser-accessible VNC on port 6080) ---
if ! pgrep -f "websockify.*${NOVNC_PORT}" > /dev/null; then
    websockify \
        --web /usr/share/novnc \
        "${NOVNC_PORT}" \
        "localhost:${VNC_PORT}" &
    echo "noVNC started — open http://localhost:${NOVNC_PORT}/vnc.html in your browser"
fi
