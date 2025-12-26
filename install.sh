#!/bin/bash
# Install Slack Caffeinator as a Login Item

set -e

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_SOURCE="$SOURCE_DIR/dist/Slack Caffeinator.app"
DESTINATION_DIR="$HOME/Applications"
APP_PATH="$DESTINATION_DIR/Slack Caffeinator.app"

# Create destination folder
mkdir -p "$DESTINATION_DIR"

# Copy the app bundle
echo "Installing Slack Caffeinator..."
rm -rf "$APP_PATH"
cp -R "$APP_SOURCE" "$APP_PATH"

# Add to Login Items using AppleScript
osascript << EOF
tell application "System Events"
    try
        delete login item "Slack Caffeinator"
    end try
    make login item at end with properties {path:"$APP_PATH", hidden:true, name:"Slack Caffeinator"}
end tell
EOF

echo ""
echo "Installed successfully!"
echo "  - App: $APP_PATH"
echo "  - Added to Login Items (runs on startup)"
echo ""
echo "Opening Slack Caffeinator..."
open "$APP_PATH"
echo "Slack Caffeinator is now running. Look for the icon in the menu bar."
echo ""
