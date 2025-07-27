#!/bin/bash

echo "Updating system packages..."
sudo apt update

echo "Installing lshw if not already installed..."
sudo apt install -y lshw

echo "Installing Python dependencies..."
pip install --user psutil

echo "Running system information script..."
python3 script.py

if [ -f "system_info.json" ]; then
    echo "✅ system_info.json created successfully!"
else
    echo "❌ Failed to create system_info.json."
fi
