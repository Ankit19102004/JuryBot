import os
import json
import PyPDF2
from openai import OpenAI
from flask import Flask, request, jsonify
try:
    from flask_cors import CORS
except ImportError:
    print("flask-cors not installed. Install with: pip install flask-cors")
    CORS = None
from werkzeug.utils import secure_filename
try:
    from config import (
        SECRET_KEY, MAX_CONTENT_LENGTH, UPLOAD_FOLDER, 
        ALLOWED_EXTENSIONS, OPENROUTER_API_KEY, MODEL_NAME,
        MAX_TOKENS, TEMPERATURE, SITE_URL, SITE_NAME, DEBUG
    )
except ImportError as e:
    print(f"Config import error: {e}")
    print("Make sure config.py exists and contains all required variables")
    # Fallback defaults
    SECRET_KEY = 'fallback-secret-key'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
    OPENROUTER_API_KEY = ''
    MODEL_NAME = 'openai/gpt-oss-20b:free'
    MAX_TOKENS = 4000
    TEMPERATURE = 0.3
    SITE_URL = 'http://localhost:5000'
    SITE_NAME = 'JuryBot'
    DEBUG = True

# Optional DOCX support
try:
    from docx import Document
    HAS_DOCX = True
except Exception:
    HAS_DOCX = False

app = Flask(__name__)
if CORS:
    CORS(app)  # Enable CORS for frontend communication

# App configuration
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure OpenAI client with OpenRouter
try:
    import os
    os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
    os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
    
    client = OpenAI()
    print("OpenAI client initialized successfully")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    try:
        # Fallback method
        client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
        print("OpenAI client initialized with fallback method")
    except Exception as e2:
        print(f"Fallback also failed: {e2}")
        client = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def extract_text_from_file(file):
    """Extract text from uploaded file"""
    filename = file.filename
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    if ext == 'pdf':
        safe_name = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
        file.save(filepath)
        try:
            text = extract_text_from_pdf(filepath)
        finally:
            try:
                os.remove(filepath)
            except Exception:
                pass
        return text

    if ext == 'txt':
        return file.read().decode('utf-8', errors='ignore')

    if ext == 'docx':
        if not HAS_DOCX:
            raise RuntimeError('DOCX processing not available. Please install python-docx.')
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    if ext == 'doc':
        raise ValueError('Legacy .doc files are not supported. Convert to PDF, TXT, or DOCX.')

    raise ValueError('Unsupported file type.')


def analyze_legal_document(text):
    """Analyze legal document using OpenAI via OpenRouter"""
    if not client:
        return {
            "error": "OpenAI client not initialized",
            "summary": "Unable to analyze document - client error",
            "risks": [],
            "terms": [],
            "recommendations": []
        }
    
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are an expert legal translator. Analyze the following legal document and provide:
                    
                    1. A simple summary (2-3 sentences)
                    2. Key risks and red flags (bullet points)
                    3. Important terms and conditions (bullet points)
                    4. Recommendations for the reader
                    
                    Document text:
                    {text[:3000]}
                    
                    Please format your response as JSON with the following structure:
                    {{
                        "summary": "Simple summary here",
                        "risks": ["Risk 1", "Risk 2"],
                        "terms": ["Term 1", "Term 2"],
                        "recommendations": ["Recommendation 1", "Recommendation 2"]
                    }}
                    """
                }
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "summary": "Unable to analyze document",
            "risks": [],
            "terms": [],
            "recommendations": []
        }


def answer_question(document_text, question):
    """Answer specific questions about the legal document"""
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are a legal expert. Answer the following question about this legal document in simple, clear language:

                    Document: {document_text[:2000]}

                    Question: {question}

                    Provide a clear, concise answer that a non-lawyer can understand.
                    """
                }
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        return completion.choices[0].message.content
    except Exception as e:
        return f"Unable to answer question: {str(e)}"


@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Handle document upload and analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        document_text = extract_text_from_file(file)

        if len(document_text) < 10:
            return jsonify({'error': 'Document appears empty or unreadable'}), 400

        analysis = analyze_legal_document(document_text)

        return jsonify({
            'success': True,
            'analysis': analysis,
            'document_length': len(document_text),
            'document_text': document_text
        })

    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@app.route('/api/analyze_text', methods=['POST'])
def analyze_text():
    """Analyze pasted text"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        if len(text) < 10:
            return jsonify({'error': 'Text too short to analyze'}), 400

        analysis = analyze_legal_document(text)

        return jsonify({
            'success': True,
            'analysis': analysis,
            'document_length': len(text)
        })

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/api/ask_question', methods=['POST'])
def ask_question():
    """Answer specific questions about the document"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        document_text = data.get('document_text', '')

        if not document_text:
            return jsonify({'error': 'No document provided'}), 400

        if not question:
            return jsonify({'error': 'No question provided'}), 400

        answer = answer_question(document_text, question)

        return jsonify({
            'success': True,
            'answer': answer,
            'question': question
        })

    except Exception as e:
        return jsonify({'error': f'Question answering failed: {str(e)}'}), 500


@app.route('/api/explain_clause', methods=['POST'])
def explain_clause():
    """Explain a specific clause or section"""
    try:
        data = request.get_json()
        clause = data.get('clause', '')
        document_text = data.get('document_text', '')

        if not document_text:
            return jsonify({'error': 'No document provided'}), 400

        if not clause:
            return jsonify({'error': 'No clause provided'}), 400

        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are a legal expert. Explain this specific clause from a legal document in simple, everyday language:

                    Clause: {clause}

                    Context from the full document: {document_text[:1000]}

                    Please explain:
                    1. What this clause means in plain English
                    2. What the implications are for the person signing
                    3. Any potential risks or concerns
                    4. What they should consider before agreeing to this

                    Format your response clearly and use simple language.
                    """
                }
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        return jsonify({
            'success': True,
            'explanation': completion.choices[0].message.content,
            'clause': clause
        })

    except Exception as e:
        return jsonify({'error': f'Clause explanation failed: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'JuryBot API is running'
    })


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)