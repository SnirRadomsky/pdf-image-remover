#!/usr/bin/env python3
"""
PDF Image Remover - Instant Launcher Generator
Creates a fast binary launcher to avoid shell overhead
"""

import os
import shutil

# Create a super minimal shell script
launcher_content = '''#!/bin/sh
export PATH="/usr/bin:/bin"
cd "/Users/snirradomsky/pdf-image-remover"
test -f venv/bin/python3 || (python3 -m venv venv; venv/bin/python3 -m pip install -r requirements.txt) >/dev/null 2>&1
curl -s http://localhost:5555/health >/dev/null 2>&1 && { open -a "Google Chrome" "http://localhost:5555"; exit; }
venv/bin/python3 app.py >/dev/null 2>&1 & sleep 3; open -a "Google Chrome" "http://localhost:5555"
wait
'''

# Write the launcher
with open('/Users/snirradomsky/Desktop/🚀 PDF - Fast Launch', 'w') as f:
    f.write(launcher_content)

# Make it executable
os.chmod('/Users/snirradomsky/Desktop/🚀 PDF - Fast Launch', 0o755)

print("✅ Created super-fast launcher: 🚀 PDF - Fast Launch")
print("📝 This launcher:")
print("   • Uses /bin/sh (no .zshrc loading)")
print("   • Minimal PATH")
print("   • Direct binary calls")
print("   • Background processes")
print("   • Should be 3-5x faster!")
