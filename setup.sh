#!/bin/bash

echo "PDF Image Remover - Setup Script"
echo "================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Check if your remove_pdf_images.py script exists
if [ -f "$HOME/scripts/remove_pdf_images.py" ]; then
    echo "✅ Found remove_pdf_images.py script at ~/scripts/"
elif [ -f "./remove_pdf_images.py" ]; then
    echo "✅ Found remove_pdf_images.py script in current directory"
else
    echo "⚠️  Warning: remove_pdf_images.py script not found!"
    echo "   Please make sure it's in ~/scripts/ or copy it to this directory"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. Run: source venv/bin/activate && python3 app.py"
echo "2. Open: http://localhost:5555"
echo "3. Or open index.html in your browser for the web interface"
echo ""
echo "Make sure your remove_pdf_images.py script is in ~/scripts/ directory"
