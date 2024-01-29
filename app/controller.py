import os
from flask import request, jsonify, Flask
from app.model import text_rank_summarize
from app.view import render_upload_form

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#Function to process the uploaded file and return the summary
def process_uploaded_file(file):
    try:
        file.seek(0)

        content = file.read().decode('utf-8')

        if not content.strip():
            return "File is empty."

        print("File Content:", content)

        summary = text_rank_summarize(content)
        return summary

    except Exception as e:
        return f"Error reading file: {str(e)}"

#Function to summarize text from a file uploaded by the user
def api_summarize():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'})

        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        summary = process_uploaded_file(file)

        return jsonify({'filename': file.filename, 'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)})

def index():
    return render_upload_form() 