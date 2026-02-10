# Code-the-Classics
Assets from the book, Code the Classics

https://magpi.raspberrypi.com/books/code-the-classics1

## Running in WSL (sound/music)

If you run these Pygame Zero games under **WSL2**, audio typically works via **WSLg** (PulseAudio), not via ALSA.

1. Ensure WSLg is available (you should have `/mnt/wslg/PulseServer`).
2. Install the runtime libraries SDL/Pygame uses for Pulse/ALSA:

	`sudo apt-get update && sudo apt-get install -y libpulse0 libasound2`

3. If sound still doesn’t start, you can force PulseAudio for a run:

	`SDL_AUDIODRIVER=pulseaudio PULSE_SERVER=unix:/mnt/wslg/PulseServer python <game>.py`

Notes:
- If you are in a container/headless environment with no audio device, SDL may fall back to a “dummy” backend (the game will run but be silent).
