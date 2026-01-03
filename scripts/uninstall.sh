#!/bin/bash
# ZWyrm Uninstallation Script

set -e

echo "🗑️  Uninstalling ZWyrm..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (sudo ./uninstall.sh)"
    exit 1
fi

# Stop and disable service
echo "🛑 Stopping service..."
systemctl stop zwyrm.service 2>/dev/null || true
systemctl disable zwyrm.service 2>/dev/null || true

# Remove systemd service
echo "🧹 Removing systemd service..."
rm -f /etc/systemd/system/zwyrm.service
systemctl daemon-reload

# Remove installed files
echo "🗑️  Removing files..."
rm -rf /opt/zwyrm
rm -rf /var/log/zwyrm

echo "✅ Uninstallation complete!"