# Keep Awake

Prevents your Mac from sleeping by wiggling the mouse every 2 minutes. Shows a ☕ icon in the menu bar.

## Install

```bash
./install.sh
```

Then add to Login Items:
1. **System Settings → General → Login Items**
2. Click **+** and select `~/Scripts/keep_awake.py`

## Run Manually

```bash
python3 keep_awake.py
```

## Configure

Edit `keep_awake.py`:
- `INTERVAL_SECONDS = 120` — how often to wiggle
- `BEEP_ENABLED = False` — set `True` for audio feedback
