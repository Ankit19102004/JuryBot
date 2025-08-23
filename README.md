# JuryBot - AI Legal Document Translator

An AI-powered tool that translates complex legal documents into simple, easy-to-understand language for the average person.

## 🎯 The Problem
Legal documents are written in specialized jargon that creates information asymmetry, putting individuals at a disadvantage when signing contracts, agreements, and terms of service.

## 🚀 The Solution
JuryBot uses AI to:
- Provide simple summaries of legal documents
- Explain complex clauses in plain language
- Identify risks and red flags
- Answer specific questions about document terms

## 🏗️ Architecture

This project is structured as a **two-part application**:

### Backend (Python Flask API)
- **Location**: `backend/` directory
- **Technology**: Python Flask with OpenRouter AI (OpenAI-compatible API)
- **Purpose**: Handles document processing, AI analysis, and API endpoints
- **Port**: 5000

### Frontend (Static Web Application)
- **Location**: `frontend/` directory
- **Technology**: HTML, CSS, JavaScript (Vanilla)
- **Purpose**: User interface and client-side functionality
- **Port**: 8080 (or any web server)

## 🛠️ Technology Stack

### Backend Technologies
- **Flask**: Web framework for API development
- **OpenAI**: Python client for AI model interactions
- **OpenRouter**: AI model provider (supports multiple AI services)
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing
- **flask-cors**: Cross-origin resource sharing

### Frontend Technologies
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **Vanilla JavaScript**: No frameworks, pure JavaScript
- **Font Awesome**: Icons
- **Google Fonts**: Inter font family

## 📁 Project Structure

```
JuryBot/
├── backend/                    # Python Flask API
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── secret.py              # Secret configuration (if exists)
│   ├── uploads/               # Temporary file storage
│   └── README.md              # Backend documentation
├── frontend/                   # Static web application
│   ├── index.html             # Main HTML file
│   ├── css/
│   │   └── style.css          # Styles and animations
│   ├── js/
│   │   └── app.js             # Frontend logic
│   └── README.md              # Frontend documentation
├── quick_start.py             # Automated setup script
├── start.py                   # Alternative startup script
├── SETUP.md                   # Detailed setup guide
└── README.md                  # This file
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
Run the quick start script that handles everything automatically:

```bash
python quick_start.py
```

This script will:
- Check your Python version
- Create a virtual environment
- Install required dependencies
- Verify your environment configuration
- Start both backend and frontend servers
- Open the application in your browser

### Option 2: Semi-Automated Setup
Use the provided scripts for easier startup:

```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Start frontend
python start.py
```

### Option 3: Manual Setup

#### Prerequisites
- Python 3.8+
- OpenRouter API key (or Google Cloud API key)
- Web browser

#### Step 1: Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "OPENROUTER_API_KEY=your-api-key-here" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env
echo "DEBUG=True" >> .env

# Start the backend server
python app.py
```

#### Step 2: Frontend Setup
```bash
# Option A: Using the provided start script (recommended)
python start.py

# Option B: Manual server
cd frontend
python -m http.server 8080
```

#### Step 3: Access the Application
- **Frontend**: Open `http://localhost:8080` in your browser
- **Backend API**: Available at `http://localhost:5000/api`

## 🔧 Configuration

### Backend Configuration
Create a `.env` file in the `backend/` directory:
```env
OPENROUTER_API_KEY=your-openrouter-api-key
SECRET_KEY=your-secret-key-here
DEBUG=True
MODEL_NAME=openai/gpt-oss-20b:free
MAX_TOKENS=4000
TEMPERATURE=0.3
```

**Note**: The application now uses OpenRouter as the primary AI provider, which provides access to various AI models including OpenAI-compatible APIs.

### Frontend Configuration
Update the API URL in `frontend/js/app.js` if needed:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## 📋 Features

### Core Functionality
- **Document Upload**: Support for PDF, TXT, DOCX files
- **Text Analysis**: Direct text input for quick analysis
- **Smart Summaries**: AI-generated plain-language summaries
- **Risk Detection**: Automatic identification of concerning clauses
- **Interactive Q&A**: Ask specific questions about document terms
- **Clause Explanation**: Get detailed explanations of specific sections

### User Experience
- **Modern UI**: Beautiful gradient design with glassmorphism effects
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Drag & Drop**: Intuitive file upload interface
- **Real-time Feedback**: Loading states and progress indicators
- **Error Handling**: Comprehensive error messages and recovery

## 🛠️ Development

### Backend Development
```bash
cd backend
python app.py
```
- API runs on `http://localhost:5000`
- Auto-reloads on code changes in debug mode

### Frontend Development
```bash
cd frontend
python -m http.server 8080
```
- Frontend runs on `http://localhost:8080`
- No build process required - just edit and refresh

### API Endpoints
- `GET /api/health` - Health check
- `POST /api/upload` - Upload and analyze document
- `POST /api/analyze_text` - Analyze pasted text
- `POST /api/ask_question` - Answer questions about document
- `POST /api/explain_clause` - Explain specific clauses

## 🎨 Design Highlights

- **Gradient Background**: Beautiful purple-blue gradient
- **Glassmorphism Cards**: Modern translucent card design
- **Smooth Animations**: Fade-in effects and hover transitions
- **Icon Integration**: Font Awesome icons throughout
- **Color-coded Results**: Different colors for risks, terms, and recommendations

## 🔒 Security & Privacy

- **No Data Storage**: Documents are processed in memory only
- **Secure API Calls**: Direct communication with AI providers
- **Environment Variables**: API keys stored securely
- **File Validation**: Type and size restrictions
- **CORS Configuration**: Proper cross-origin resource sharing

## 📱 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🚀 Production Deployment

### Backend Deployment
1. Set `DEBUG=False` in `.env`
2. Use production WSGI server (Gunicorn)
3. Configure proper CORS origins
4. Set up HTTPS

### Frontend Deployment
1. Update API URL to production backend
2. Deploy to any static hosting service
3. Configure caching headers
4. Enable compression

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## 📞 Support

For detailed setup instructions, see `SETUP.md`
For backend-specific help, see `backend/README.md`
For frontend-specific help, see `frontend/README.md`