# Code-the-Classics
Assets from the book, Code the Classics

https://magpi.raspberrypi.com/books/code-the-classics1

## Running in GitHub Codespaces

This repository is configured for GitHub Codespaces with a graphical desktop for running the Pygame Zero games.

1. Click the green "Code" button on GitHub and select "Open with Codespaces"
2. Create a new codespace (the environment will set up automatically)
3. Once ready, open the "Desktop (noVNC)" port (6080) from the Ports tab - it should open automatically
4. In the noVNC browser window, click "Connect" (password: `codespaces`)
5. Open a terminal in VS Code and run a game:

```bash
cd boing-master && python boing.py
```

The game window will appear in the noVNC desktop viewer. Audio is disabled in Codespaces (games run silently).

**Available games:**
- `boing-master/boing.py` - Pong clone
- `cavern-master/cavern.py` - Bubble Bobble-style platformer
- `soccer-master/soccer.py` - Soccer simulation
- `bunner-master/bunner.py` - Frogger clone
- `myriapod-master/myriapod.py` - Centipede clone

## Running in WSL (sound/music)

If you run these Pygame Zero games under **WSL2**, audio typically works via **WSLg** (PulseAudio), not via ALSA.

1. Ensure WSLg is available (you should have `/mnt/wslg/PulseServer`).
2. Install the runtime libraries SDL/Pygame uses for Pulse/ALSA:

	`sudo apt-get update && sudo apt-get install -y libpulse0 libasound2`

3. If sound still doesn’t start, you can force PulseAudio for a run:

	`SDL_AUDIODRIVER=pulseaudio PULSE_SERVER=unix:/mnt/wslg/PulseServer python <game>.py`

Notes:
- If you are in a container/headless environment with no audio device, SDL may fall back to a “dummy” backend (the game will run but be silent).
