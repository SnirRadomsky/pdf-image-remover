#!/bin/bash

echo "🚀 Starting PDF Image Remover Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment and start server
source venv/bin/activate
python3 app.py
