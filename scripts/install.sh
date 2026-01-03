#!/bin/bash
# ZWyrm Installation Script

set -e

echo "🚀 Installing ZWyrm Behavioral Antivirus..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (sudo ./install.sh)"
    exit 1
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p /opt/zwyrm
mkdir -p /opt/zwyrm/config
mkdir -p /opt/zwyrm/logs
mkdir -p /var/log/zwyrm

# Copy files
echo "📄 Copying files..."
cp -r * /opt/zwyrm/ 2>/dev/null || true

# Set permissions
echo "🔒 Setting permissions..."
chmod 755 /opt/zwyrm
chmod 644 /opt/zwyrm/config/zwyrm.yaml
chmod 755 /opt/zwyrm/main.py
chmod 755 /opt/zwyrm/scripts/*.sh

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r /opt/zwyrm/requirements.txt

# Install systemd service
echo "⚙️ Installing systemd service..."
if [ -f /opt/zwyrm/systemd/zwyrm.service ]; then
    cp /opt/zwyrm/systemd/zwyrm.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable zwyrm.service
    echo "✅ Service installed and enabled"
else
    echo "⚠️  Systemd service file not found, skipping"
fi

echo "✨ Installation complete!"
echo ""
echo "To start ZWyrm:"
echo "  sudo systemctl start zwyrm"
echo ""
echo "To check status:"
echo "  sudo systemctl status zwyrm"
echo ""
echo "To view logs:"
echo "  sudo tail -f /var/log/zwyrm/zwyrm.log"