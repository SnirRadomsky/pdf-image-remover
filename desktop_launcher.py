#!/usr/bin/env python3
"""
PDF Image Remover - Desktop Launcher
Creates a simple local web interface to control the main app
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path
from flask import Flask, render_template_string, jsonify, redirect
import webbrowser

app = Flask(__name__)
main_app_process = None
APP_DIR = "/Users/snirradomsky/pdf-image-remover"

LAUNCHER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PDF Image Remover - Desktop Launcher</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }
        .launcher {
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 600px;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333;
        }
        .status {
            margin: 20px 0;
            padding: 15px;
            border-radius: 10px;
            font-weight: 600;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .launch-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 20px 40px;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: 600;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        .launch-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        .launch-btn.success {
            background: linear-gradient(135deg, #28a745, #20c997);
        }
    </style>
</head>
<body>
    <div class="launcher">
        <div class="title">📄 PDF Image Remover</div>
        
        {% if server_running %}
            <div class="status success">
                ✅ PDF Image Remover is running and ready!
            </div>
            <a href="http://localhost:5555" target="_blank" class="launch-btn success">
                🌐 Open PDF Image Remover
            </a>
            <br><br>
            <a href="/stop" class="launch-btn" style="background: #dc3545;">
                🛑 Stop Server
            </a>
        {% else %}
            <div class="status info">
                ⭕ PDF Image Remover server is not running
            </div>
            <a href="/start" class="launch-btn">
                🚀 Start PDF Image Remover
            </a>
        {% endif %}
        
        <div style="margin-top: 30px; color: #666; font-size: 0.9rem;">
            <p>This page refreshes automatically every 5 seconds</p>
            <p>Server status: {{ "Running" if server_running else "Stopped" }}</p>
        </div>
    </div>
</body>
</html>
"""

def is_server_running():
    """Check if the main PDF Image Remover server is running"""
    try:
        import urllib.request
        urllib.request.urlopen('http://localhost:5555/health', timeout=2)
        return True
    except:
        return False

def start_main_app():
    """Start the main PDF Image Remover application"""
    global main_app_process
    
    if main_app_process and main_app_process.poll() is None:
        return True
    
    try:
        os.chdir(APP_DIR)
        # Start the main app
        cmd = ["./venv/bin/python3", "app.py"]
        main_app_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )
        
        # Wait a moment for it to start
        time.sleep(3)
        return is_server_running()
        
    except Exception as e:
        print(f"Error starting app: {e}")
        return False

def stop_main_app():
    """Stop the main PDF Image Remover application"""
    global main_app_process
    
    try:
        if main_app_process and main_app_process.poll() is None:
            os.killpg(os.getpgid(main_app_process.pid), signal.SIGTERM)
            main_app_process = None
        
        # Also try to kill any remaining processes
        subprocess.run(["pkill", "-f", "python3 app.py"], capture_output=True)
        
        return True
    except Exception as e:
        print(f"Error stopping app: {e}")
        return False

@app.route('/')
def index():
    return render_template_string(LAUNCHER_HTML, server_running=is_server_running())

@app.route('/start')
def start():
    success = start_main_app()
    time.sleep(2)  # Give it time to start
    return redirect('/')

@app.route('/stop')
def stop():
    stop_main_app()
    time.sleep(1)
    return redirect('/')

@app.route('/status')
def status():
    return jsonify({'running': is_server_running()})

def cleanup_on_exit():
    """Cleanup function to stop the main app when launcher exits"""
    stop_main_app()

if __name__ == '__main__':
    # Set up cleanup on exit
    import atexit
    atexit.register(cleanup_on_exit)
    
    print("🎯 PDF Image Remover - Desktop Launcher")
    print("=====================================")
    print("🌐 Opening launcher in browser...")
    print("📝 Use the web interface to start/stop the PDF Image Remover")
    print("🛑 Close this terminal to stop the launcher")
    print("")
    
    # Open browser after a short delay
    threading.Timer(1.0, lambda: webbrowser.open('http://localhost:8888')).start()
    
    # Start the launcher web interface
    try:
        app.run(host='127.0.0.1', port=8888, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down launcher...")
        cleanup_on_exit()
