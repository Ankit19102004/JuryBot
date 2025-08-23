import os
import ast
from dotenv import load_dotenv

# Load environment variables from backend/.env
BASE_DIR = os.path.dirname(__file__)
load_dotenv(os.path.join(BASE_DIR, '.env'))

def get_bool(name, default=False):
    """Helper function to parse boolean environment variables"""
    value = os.getenv(name)
    if value is None:
        return default
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')

def get_int(name, default_value):
    """Helper function to parse integer environment variables"""
    try:
        return int(os.getenv(name, default_value))
    except Exception:
        return default_value

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', 'OpenRouter API Key')
SITE_URL = os.getenv('SITE_URL', 'http://localhost:5000')  # Optional for OpenRouter rankings
SITE_NAME = os.getenv('SITE_NAME', 'Lawlens')  # Optional for OpenRouter rankings

# AI Model Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'openai/gpt-oss-20b:free')
MAX_TOKENS = get_int('MAX_TOKENS', 4000)
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.3'))

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'b1ce3f53e0ef70564b4b8fa8a4aad34de21987f151bca587867f83e3c9ce5aea')
DEBUG = get_bool('DEBUG', True)

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",  # React development server
    "http://localhost:8080",  # Vue development server
    "http://localhost:4200",  # Angular development server
    "http://127.0.0.1:5500",  # Live Server
    "http://localhost:5500",  # Live Server alternative
    "http://127.0.0.1:3000",  # React alternative
]

# File Upload Configuration
MAX_CONTENT_LENGTH = get_int('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)  # 16MB default
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, '..', 'temp'))

# Allowed extensions parsing from string or list
raw_allowed = os.getenv('ALLOWED_EXTENSIONS', "pdf,txt,docx")
try:
    if raw_allowed.strip().startswith('['):
        ALLOWED_EXTENSIONS = set(ast.literal_eval(raw_allowed))
    else:
        ALLOWED_EXTENSIONS = set([ext.strip().lower() for ext in raw_allowed.split(',') if ext.strip()])
except Exception:
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}