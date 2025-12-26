#!/bin/bash
# Install Slack Caffeinator as a Login Item

set -e

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_PATH="$SOURCE_DIR/slack_caffeinator.py"
DESTINATION_DIR="$HOME/Scripts"
DESTINATION_PATH="$DESTINATION_DIR/slack_caffeinator.py"
APP_PATH="$DESTINATION_DIR/Slack Caffeinator.app"

# Create Scripts folder
mkdir -p "$DESTINATION_DIR"

# Copy script
cp "$SOURCE_PATH" "$DESTINATION_PATH"
chmod +x "$DESTINATION_PATH"

# Install dependencies using homebrew python
echo "Installing dependencies..."
/opt/homebrew/bin/pip3 install rumps pyobjc-framework-Quartz pyautogui 2>/dev/null || \
    pip3 install --break-system-packages rumps pyobjc-framework-Quartz pyautogui 2>/dev/null || \
    pip3 install rumps pyobjc-framework-Quartz pyautogui

# Create app bundle
mkdir -p "$APP_PATH/Contents/MacOS"

# Create launcher executable
cat > "$APP_PATH/Contents/MacOS/Slack Caffeinator" << EOF
#!/bin/bash
/opt/homebrew/bin/python3 $DESTINATION_PATH
EOF
chmod +x "$APP_PATH/Contents/MacOS/Slack Caffeinator"

# Create Info.plist (LSUIElement hides from Dock)
cat > "$APP_PATH/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Slack Caffeinator</string>
    <key>CFBundleIdentifier</key>
    <string>com.cperkins.slackcaffeinator</string>
    <key>CFBundleName</key>
    <string>Slack Caffeinator</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSUIElement</key>
    <true/>
</dict>
</plist>
EOF

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
echo "✓ Installed successfully!"
echo "  - Script: $DESTINATION_PATH"
echo "  - App: $APP_PATH"
echo "  - Added to Login Items (runs on startup)"
echo ""
echo "Opening Slack Caffeinator..."
open "$APP_PATH"
echo "Slack Caffeinator is now running. Look for the ☕ icon in the menu bar."
echo ""