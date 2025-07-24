# PDF Image Remover Web Application

A modern web application for removing images from PDF files while preserving text content and formatting.

## Features

- 🎨 **Modern UI** - Clean, responsive design with drag & drop support
- 📄 **PDF Processing** - Uses your proven Python script for reliable image removal
- 🔒 **Secure** - Server-side processing with automatic file cleanup
- 📱 **Responsive** - Works on desktop and mobile devices
- ⚡ **Fast** - Efficient processing with progress indicators
- 🗂️ **Easy** - Simple drag & drop or click to upload

## Prerequisites

- Python 3.6+
- Your existing `remove_pdf_images.py` script (should be in `~/scripts/` directory)

## Quick Start

1. **Setup the application:**
   ```bash
   cd /Users/snirradomsky/pdf-image-remover
   ./setup.sh
   ```

2. **Start the server:**
   ```bash
   ./start.sh
   # OR manually:
   source venv/bin/activate && python3 app.py
   ```

3. **Open the web interface:**
   - Navigate to `http://localhost:5555` in your browser
   - Or open `index.html` directly in your browser

## How It Works

1. **Upload**: Drag & drop or click to select a PDF file
2. **Process**: Click "Remove Images" to process the file
3. **Download**: Get your processed PDF with images removed

## File Structure

```
pdf-image-remover/
├── app.py              # Flask backend server
├── index.html          # Web interface
├── requirements.txt    # Python dependencies
├── setup.sh           # Setup script
└── README.md          # This file
```

## API Endpoints

- `GET /` - Main page
- `GET /health` - Server health check
- `POST /api/remove-images` - Process PDF file

## Configuration

The application looks for your `remove_pdf_images.py` script in these locations:
1. `~/scripts/remove_pdf_images.py` (recommended)
2. `./remove_pdf_images.py` (current directory)
3. `./scripts/remove_pdf_images.py`
4. `../scripts/remove_pdf_images.py`

## Troubleshooting

### Server Won't Start
- Make sure all dependencies are installed: `pip3 install -r requirements.txt`
- Check if port 5000 is available
- Verify Python 3 is installed: `python3 --version`

### Script Not Found Error
- Ensure `remove_pdf_images.py` is in `~/scripts/` directory
- Check script permissions: `chmod +x ~/scripts/remove_pdf_images.py`
- Verify the script works independently

### Upload Fails
- Check file size (max 50MB)
- Ensure file is a valid PDF
- Check server logs for detailed errors

## Development

To modify the application:

1. **Frontend**: Edit `index.html` for UI changes
2. **Backend**: Edit `app.py` for server logic
3. **Styling**: CSS is embedded in `index.html`

## Security Notes

- Files are processed server-side and automatically cleaned up
- No files are permanently stored on the server
- Maximum file size limit of 50MB
- Only PDF files are accepted

## License

This application integrates with your existing PDF processing script and provides a modern web interface for it.
