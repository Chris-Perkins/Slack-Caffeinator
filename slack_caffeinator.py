#!/usr/bin/env python3
"""
Slack Caffeinator - Keeps your Slack status 'Online' by gently wiggling the mouse.
Shows a ☕ icon in the menu bar when running.
"""

import subprocess
import threading
import time
from datetime import datetime

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
CAFFEINATION_INTERVAL_SECONDS = 120
"""
How often to check if we should caffeinate.
"""
IDLE_THRESHOLD_SECONDS = 60
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
                self._caffeinate()
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

    def _caffeinate(self):
        """
        Prevent display and idle sleep using:
        1. macOS caffeinate command (keeps screen awake)
        2. Moving the mouse around (registers as activity for Slack)
        """
        subprocess.Popen(["caffeinate", "-d", "-i", "-t", str(self.interval_seconds)])

        event = Quartz.CGEventCreate(None)
        current_pos = Quartz.CGEventGetLocation(event)
        offsets = [(50, 0), (0, 50), (-50, 0), (0, -50)]

        for dx, dy in offsets:
            new_x = current_pos.x + dx
            new_y = current_pos.y + dy

            move_event = Quartz.CGEventCreateMouseEvent(
                None,
                Quartz.kCGEventMouseMoved,
                (new_x, new_y),
                Quartz.kCGMouseButtonLeft,
            )
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, move_event)
            current_pos = Quartz.CGPoint(new_x, new_y)
            time.sleep(0.05)

        Quartz.CGEventCreateMouseEvent(
            None,
            Quartz.kCGEventMouseMoved,
            current_pos,
            Quartz.kCGMouseButtonLeft,
        )


if __name__ == "__main__":
    app = KeepAwakeApp(
        interval_seconds=CAFFEINATION_INTERVAL_SECONDS,
        idle_threshold_seconds=IDLE_THRESHOLD_SECONDS,
        is_beep_enabled=IS_DEBUG_BEEP_ENABLED,
    )
    app.run()
