#!/bin/bash
# Install Keep Awake as a Login Item

set -e

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_PATH="$SOURCE_DIR/slack_caffeinator.py"
DESTINATION_DIR="$HOME/Scripts"
DESTINATION_PATH="$DESTINATION_DIR/slack_caffeinator.py"
WRAPPER_PATH="$DESTINATION_DIR/Slack Caffeinator"

# Create Scripts folder
mkdir -p "$DESTINATION_DIR"

# Copy script
cp "$SOURCE_PATH" "$DESTINATION_PATH"
chmod +x "$DESTINATION_PATH"

# Install rumps using homebrew python
echo "Installing dependencies..."
/opt/homebrew/bin/pip3 install rumps 2>/dev/null || pip3 install --break-system-packages rumps 2>/dev/null || pip3 install rumps

# Create a launcher wrapper (Login Items needs an app or .command file)
cat > "$WRAPPER_PATH" << 'EOF'
#!/bin/bash
/opt/homebrew/bin/python3 "$HOME/Scripts/slack_caffeinator.py"
EOF
chmod +x "$WRAPPER_PATH"

# Add to Login Items using AppleScript
osascript << EOF
tell application "System Events"
    try
        delete login item "Slack Caffeinator"
    end try
    make login item at end with properties {path:"$WRAPPER_PATH", hidden:true, name:"Slack Caffeinator"}
end tell
EOF

echo ""
echo "✓ Installed successfully!"
echo "  - Script: $DESTINATION_PATH"
echo "  - Launcher: $WRAPPER_PATH"
echo "  - Added to Login Items (runs on startup)"
echo ""
echo "To run now: python3 $DESTINATION_PATH"
