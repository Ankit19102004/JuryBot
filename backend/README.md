# JuryBot Backend API

This is the backend API for the JuryBot legal document translator application.

## Features

- **Document Analysis**: Upload and analyze legal documents using OpenRouter AI
- **Text Analysis**: Analyze pasted legal text
- **Question Answering**: Ask specific questions about documents
- **Clause Explanation**: Get detailed explanations of specific clauses
- **CORS Support**: Cross-origin resource sharing enabled for frontend communication

## API Endpoints

### Health Check
- `GET /api/health` - Check if the API is running

### Document Analysis
- `POST /api/upload` - Upload and analyze a legal document file
- `POST /api/analyze_text` - Analyze pasted legal text

### Interactive Features
- `POST /api/ask_question` - Ask questions about a document
- `POST /api/explain_clause` - Explain specific clauses

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your-api-key-here
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   MODEL_NAME=openai/gpt-oss-20b:free
   MAX_TOKENS=4000
   TEMPERATURE=0.3
   ```

3. Run the server:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Documentation

### Upload Document
```bash
POST /api/upload
Content-Type: multipart/form-data

file: [PDF, TXT, DOCX file]
```

### Analyze Text
```bash
POST /api/analyze_text
Content-Type: application/json

{
  "text": "Legal document text here..."
}
```

### Ask Question
```bash
POST /api/ask_question
Content-Type: application/json

{
  "question": "What happens if I'm late on a payment?",
  "document_text": "Full document text..."
}
```

### Explain Clause
```bash
POST /api/explain_clause
Content-Type: application/json

{
  "clause": "Specific clause text...",
  "document_text": "Full document text..."
}
```

## Response Format

All endpoints return JSON responses with the following structure:

```json
{
  "success": true,
  "analysis": {
    "summary": "Document summary...",
    "risks": ["Risk 1", "Risk 2"],
    "terms": ["Term 1", "Term 2"],
    "recommendations": ["Recommendation 1", "Recommendation 2"]
  }
}
```

## Error Handling

Errors are returned with appropriate HTTP status codes:

```json
{
  "error": "Error message description"
}
```

## CORS Configuration

The API is configured to accept requests from common frontend development servers:
- `http://localhost:3000` (React)
- `http://localhost:8080` (Vue)
- `http://localhost:4200` (Angular)
- `http://localhost:5500` (Live Server)

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

## Production

For production deployment:
1. Set `DEBUG=False` in your `.env` file
2. Use a production WSGI server like Gunicorn
3. Configure proper CORS origins for your domain

## AI Provider

This backend uses OpenRouter as the AI provider, which gives access to various AI models including:
- OpenAI GPT models
- Anthropic Claude models
- Google Gemini models
- And many others

You can change the model by updating the `MODEL_NAME` in your `.env` file.
