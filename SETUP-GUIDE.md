# PDF Image Remover - Clean Setup Guide

## 🗂️ Organized Structure

### Main Application
- **Location**: `/Users/snirradomsky/workspace/pdf-image-remover/`
- **Contains**: Web interface, Python backend, virtual environment

### Launcher Script
- **Location**: `~/scripts/pdf-image-remover-launch.sh`
- **Fast startup**: Uses `/bin/bash` with minimal environment to avoid .zshrc loading

### Alias
- **Command**: `pdf-remover`
- **Added to**: `~/.zshrc`
- **Usage**: Type `pdf-remover` in any terminal

## 🚀 How to Use

### Option 1: Terminal Command (Fastest)
```bash
pdf-remover
```

### Option 2: Desktop Shortcut
Double-click: `📄 PDF Image Remover.command` on Desktop

### Option 3: Direct Script
```bash
~/scripts/pdf-image-remover-launch.sh
```

## ⚡ Performance Features

- ✅ Uses `/bin/bash` instead of zsh (avoids .zshrc loading)
- ✅ Minimal PATH environment 
- ✅ Direct binary calls (`/usr/bin/curl`, `/usr/bin/open`)
- ✅ Background server startup
- ✅ Smart caching (checks if already running)
- ✅ Fast Chrome launch

## 🎯 What It Does

1. **Checks** if server is already running (instant if yes)
2. **Sets up** virtual environment (first time only)
3. **Starts** PDF Image Remover server in background
4. **Opens** beautiful web interface in Chrome
5. **Ready** to drag & drop PDF files!

## 📁 Files Kept

- `~/scripts/pdf-image-remover-launch.sh` - Main launcher
- `~/scripts/remove_pdf_images.py` - PDF processing script
- `/Users/snirradomsky/workspace/pdf-image-remover/` - Web application
- `📄 PDF Image Remover.command` - Desktop shortcut

## 🗑️ Files Cleaned Up

Removed all the duplicate launchers and test files from Desktop:
- Various .command files
- HTML launchers  
- AppleScript files
- Test outputs
- PDF Image Remover.app

---

**Quick Start**: Just type `pdf-remover` in terminal! 🚀
