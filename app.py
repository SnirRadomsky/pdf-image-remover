#!/usr/bin/env python3
"""
PDF Image Remover Web Application Backend
Integrates with the existing remove_pdf_images.py script
"""

import os
import tempfile
import subprocess
import sys
from pathlib import Path
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_script_path():
    """Get the path to the remove_pdf_images.py script"""
    script_path = Path.home() / 'scripts' / 'remove_pdf_images.py'
    if script_path.exists():
        return str(script_path)
    
    # Alternative locations to check
    alternative_paths = [
        Path('./remove_pdf_images.py'),
        Path('./scripts/remove_pdf_images.py'),
        Path('../scripts/remove_pdf_images.py')
    ]
    
    for path in alternative_paths:
        if path.exists():
            return str(path)
    
    raise FileNotFoundError("remove_pdf_images.py script not found")

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_file('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        script_path = get_script_path()
        return jsonify({
            'status': 'healthy',
            'script_found': True,
            'script_path': script_path
        })
    except FileNotFoundError as e:
        return jsonify({
            'status': 'error',
            'script_found': False,
            'error': str(e)
        }), 500

@app.route('/api/remove-images', methods=['POST'])
def remove_images():
    """Process PDF to remove images"""
    try:
        # Check if file was uploaded
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['pdf_file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        logger.info(f"Processing file: {file.filename}")
        
        # Generate unique filenames
        original_filename = secure_filename(file.filename)
        input_filename = f"input_{original_filename}"
        output_filename = f"output_{original_filename}"
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        try:
            # Save uploaded file
            file.save(input_path)
            logger.info(f"File saved to: {input_path}")
            
            # Get the script path
            script_path = get_script_path()
            logger.info(f"Using script: {script_path}")
            
            # Run the remove_pdf_images.py script
            cmd = [sys.executable, script_path, input_path, output_path]
            logger.info(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Script failed with return code {result.returncode}")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                return jsonify({
                    'error': 'Failed to process PDF',
                    'details': result.stderr
                }), 500
            
            logger.info(f"Script completed successfully: {result.stdout}")
            
            # Check if output file was created
            if not os.path.exists(output_path):
                logger.error(f"Output file not created: {output_path}")
                return jsonify({'error': 'Output file was not created'}), 500
            
            # Send the processed file
            return send_file(
                output_path,
                as_attachment=True,
                download_name=original_filename.replace('.pdf', '_no_images.pdf'),
                mimetype='application/pdf'
            )
            
        finally:
            # Clean up temporary files
            for temp_file in [input_path, output_path]:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        logger.info(f"Cleaned up: {temp_file}")
                except Exception as e:
                    logger.warning(f"Failed to clean up {temp_file}: {e}")
    
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Processing timeout - file too large or complex'}), 408
    except FileNotFoundError as e:
        logger.error(f"Script not found: {e}")
        return jsonify({'error': 'PDF processing script not found'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 50MB.'}), 413

if __name__ == '__main__':
    print("Starting PDF Image Remover Server...")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    
    try:
        script_path = get_script_path()
        print(f"Found script at: {script_path}")
    except FileNotFoundError as e:
        print(f"WARNING: {e}")
        print("Make sure your remove_pdf_images.py script is in ~/scripts/ or current directory")
    
    print("Server starting on http://localhost:5555")
    app.run(debug=True, host='0.0.0.0', port=5555)
