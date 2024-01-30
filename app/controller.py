# app/controller.py

import os
import PyPDF2
from flask import request, jsonify, Flask
from app.model import text_rank_summarize
from app.view import render_upload_form

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#Função que extrai texto de um arquivo PDF
def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    try:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found: {pdf_file}")
    return pdf_text

#Função que processa um arquivo enviado pelo usuário, caso seja um arquivo PDF, 
#extrai o texto e o resume, caso seja um arquivo de texto, apenas resume o texto
def process_uploaded_file(content, is_pdf=False):
    try:
        if is_pdf:
            text = extract_text_from_pdf(content)
        else:
            text = content.decode('utf-8')

        if not text.strip():
            return "File is empty."

        return text_rank_summarize(text)

    except Exception as e:
        return f"Error reading file: {str(e)}"

#Função que processa a requisição de resumo de um arquivo enviado pelo usuário
def api_summarize():
    try:
        #Verifica se o arquivo foi enviado pelo usuário
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo fornecido'})

        #Obtém o arquivo enviado pelo usuário e a chave de API
        file = request.files['file']
        api_key = request.headers.get('Api-Key')

        #Verifica se o arquivo e a chave de API foram fornecidos
        if file.filename == '' or not api_key:
            return jsonify({'error': 'Nenhum arquivo selecionado ou chave de API fornecida'})

        #Verifica se o arquivo é um tipo permitido
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não permitido. Apenas arquivos .txt e .pdf são aceitos.'})

        #Salva o arquivo no diretório de uploads
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        #Verifica se o arquivo é um PDF
        is_pdf = file.filename.lower().endswith('.pdf')
        summary = process_uploaded_file(filename, is_pdf)

        return jsonify({'filename': file.filename, 'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)})

#Função que renderiza o formulário de upload da view
def index():
    return render_upload_form()
