#!/usr/bin/env python3
"""
Slack Caffeinator - Keeps your Slack status 'Online' by gently wiggling the mouse.
Shows a ☕ icon in the menu bar when running.
"""

import subprocess
import threading
import time
from datetime import datetime


import pyautogui
import Quartz
import rumps
from AppKit import NSApplication, NSApplicationActivationPolicyAccessory

# Run in the background, hidden from the application dock
NSApplication.sharedApplication().setActivationPolicy_(
    NSApplicationActivationPolicyAccessory
)

# =============================================================================
# Configuration
# =============================================================================

IS_DEBUG_BEEP_ENABLED = False
"""
If True, will beep when caffeinating the screen.
"""
CAFFEINATION_INTERVAL_SECONDS = 2 * 60
"""
How often to check if we should caffeinate.
"""
IDLE_THRESHOLD_SECONDS = 2 * 60
"""
Caffeinate if idle for at least this many seconds.
"""

# =============================================================================
# Application
# =============================================================================


class KeepAwakeApp(rumps.App):
    def __init__(
        self,
        interval_seconds: float,
        idle_threshold_seconds: float,
        is_beep_enabled: bool,
    ):
        super().__init__("I'm Awake!", title="☕")
        self.interval_seconds = interval_seconds
        self.idle_threshold_seconds = idle_threshold_seconds
        self.is_beep_enabled = is_beep_enabled

        self.menu = [
            rumps.MenuItem("Slack Caffeinator: Active", callback=None),
        ]

        self.caffeination_thread = threading.Thread(
            target=self._caffeination_loop,
            daemon=True,
        )
        self.caffeination_thread.start()

    def _caffeination_loop(self):
        print(f"[{datetime.now()}] Slack Caffeinator running")
        while True:
            idle_time = self._get_seconds_since_last_user_input()

            if idle_time >= self.idle_threshold_seconds:
                self._caffeinate_slack()
                if self.is_beep_enabled:
                    self._play_beep()
                print(f"[{datetime.now()}] Caffeinated")
            else:
                print(f"[{datetime.now()}] User active, skipping caffeination")

            time.sleep(self.interval_seconds)

    def _get_seconds_since_last_user_input(self):
        """Get seconds since last user input (mouse/keyboard)."""
        return Quartz.CGEventSourceSecondsSinceLastEventType(
            Quartz.kCGEventSourceStateHIDSystemState,
            Quartz.kCGAnyInputEventType,
        )

    def _play_beep(self):
        """Play a basic beep sound using macOS afplay."""
        subprocess.run(
            ["afplay", "/System/Library/Sounds/Tink.aiff"],
            capture_output=True,
        )

    def _caffeinate_slack(self):
        """
        Prevent display and idle sleep by:
        1. Running the macOS caffeinate command to keep the screen awake
        2. Wiggling the mouse
        """
        subprocess.Popen(["caffeinate", "-d", "-i", "-t", str(self.interval_seconds)])
        self._wiggle_mouse()

    def _wiggle_mouse(self):
        """Move mouse in a small pattern and return to original position."""

        pyautogui.FAILSAFE = False

        original_x, original_y = pyautogui.position()
        time_to_move_cursor = 0.00005

        dxdy = [(50, 50), (-50, -50), (200, 200), (-200, -200)]
        for dx, dy in dxdy:
            pyautogui.moveTo(
                x=original_x + dx,
                y=original_y + dy,
                duration=1,
            )
        pyautogui.moveTo(original_x, original_y, duration=time_to_move_cursor)


if __name__ == "__main__":
    app = KeepAwakeApp(
        interval_seconds=CAFFEINATION_INTERVAL_SECONDS,
        idle_threshold_seconds=IDLE_THRESHOLD_SECONDS,
        is_beep_enabled=IS_DEBUG_BEEP_ENABLED,
    )
    app.run()
