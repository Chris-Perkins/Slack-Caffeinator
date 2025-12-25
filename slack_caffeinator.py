#!/usr/bin/env python3
"""
Keep Awake - Prevents monitor from sleeping by simulating small mouse movements.
Shows a menu bar icon when running.
"""

import subprocess
import sys
import threading
import time
from datetime import datetime

import rumps
from AppKit import NSApplication, NSApplicationActivationPolicyAccessory

# Hide from Dock
NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyAccessory)

# =============================================================================
# Configuration
# =============================================================================

BEEP_ENABLED = False
INTERVAL_SECONDS = 120


# =============================================================================
# Application
# =============================================================================


class KeepAwakeApp(rumps.App):
    def __init__(
        self,
        interval_seconds: float,
        is_beep_enabled: bool,
    ):
        super().__init__("I'm Awake!", title="☕")
        self.interval_seconds = interval_seconds
        self.is_beep_enabled = is_beep_enabled

        self.menu = [
            rumps.MenuItem("Status: Active", callback=None),
            rumps.MenuItem(f"Interval: {interval_seconds} seconds", callback=None),
        ]

        self.wiggle_thread = threading.Thread(target=self.wiggle_loop, daemon=True)
        self.wiggle_thread.start()

    def wiggle_loop(self):
        while True:
            self.move_mouse()
            if self.is_beep_enabled:
                self.play_beep()
            current_time = datetime.now()
            print(f"[{current_time}] Mouse wiggled")
            time.sleep(self.interval_seconds)

    def play_beep(self):
        """Play a basic beep sound using macOS afplay."""
        subprocess.run(
            ["afplay", "/System/Library/Sounds/Tink.aiff"], capture_output=True
        )

    def move_mouse(self):
        """Move the mouse slightly using AppleScript (macOS)."""
        subprocess.run(
            [
                "osascript",
                "-e",
                """
        tell application "System Events"
            set mousePos to do shell script "python3 -c 'import Quartz; pos = Quartz.NSEvent.mouseLocation(); print(int(pos.x), int(1080 - pos.y))'"
            set {x, y} to words of mousePos
            set x to x as integer
            set y to y as integer
            -- Move mouse 1 pixel and back
            do shell script "python3 -c 'import Quartz; from Quartz import CGEventCreateMouseEvent, kCGEventMouseMoved, CGEventPost, kCGHIDEventTap; e = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (" & (x + 1) & ", " & y & "), 0); CGEventPost(kCGHIDEventTap, e)'"
            delay 0.1
            do shell script "python3 -c 'import Quartz; from Quartz import CGEventCreateMouseEvent, kCGEventMouseMoved, CGEventPost, kCGHIDEventTap; e = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (" & x & ", " & y & "), 0); CGEventPost(kCGHIDEventTap, e)'"
        end tell
        """,
            ],
            capture_output=True,
        )


if __name__ == "__main__":
    print(f"Keep Awake running - wiggling mouse every {INTERVAL_SECONDS} seconds")
    if BEEP_ENABLED:
        print("Beeping is enabled")

    app = KeepAwakeApp(
        interval_seconds=INTERVAL_SECONDS,
        is_beep_enabled=BEEP_ENABLED,
    )
    app.run()
