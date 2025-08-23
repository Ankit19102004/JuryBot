# JuryBot Setup Guide

## Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://python.org)
2. **OpenRouter Account** - Sign up at [openrouter.ai](https://openrouter.ai)
3. **OpenRouter API Key** - You'll need to get an API key from OpenRouter
4. **Web Browser** - Any modern browser (Chrome, Firefox, Safari, Edge)

## Step 1: Get Your OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to your API keys section
4. Create a new API key
5. Copy the generated API key

**Note**: OpenRouter provides access to various AI models including OpenAI GPT, Anthropic Claude, Google Gemini, and many others. You can choose different models by updating the `MODEL_NAME` in your configuration.

## Step 2: Backend Setup

### Install Backend Dependencies
```bash
# Navigate to the backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt
```

### Configure Backend
Create a `.env` file in the `backend/` directory:

**On Windows:**
```bash
echo OPENROUTER_API_KEY=your-api-key-here > .env
echo SECRET_KEY=your-secret-key-here >> .env
echo DEBUG=True >> .env
echo MODEL_NAME=openai/gpt-oss-20b:free >> .env
echo MAX_TOKENS=4000 >> .env
echo TEMPERATURE=0.3 >> .env
```

**On macOS/Linux:**
```bash
cat > .env << EOF
OPENROUTER_API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here
DEBUG=True
MODEL_NAME=openai/gpt-oss-20b:free
MAX_TOKENS=4000
TEMPERATURE=0.3
EOF
```

Replace `your-api-key-here` with your actual OpenRouter API key.

### Start Backend Server
```bash
# Make sure you're in the backend directory
cd backend

# Start the Flask server
python app.py
```

The backend API will be available at: **http://localhost:5000**

## Step 3: Frontend Setup

### Option A: Using the provided start script (Recommended)
```bash
# From the project root directory
python start.py
```

### Option B: Manual server
Open a **new terminal window** and run:

```bash
# Navigate to the frontend directory
cd frontend

# Start a simple web server
python -m http.server 8080
```

The frontend will be available at: **http://localhost:8080**

## Step 4: Test the Application

1. Open your web browser and go to `http://localhost:8080`
2. You should see the JuryBot interface
3. Try uploading a legal document or pasting some legal text
4. The AI should analyze the document and provide insights

## Alternative Frontend Servers

If you prefer different frontend servers:

### Using Node.js
```bash
cd frontend
npx serve .
```

### Using Live Server (VS Code)
1. Install the "Live Server" extension in VS Code
2. Right-click on `frontend/index.html`
3. Select "Open with Live Server"

### Using PHP
```bash
cd frontend
php -S localhost:8080
```

## Troubleshooting

### Common Issues

**1. "Module not found" errors (Backend)**
```bash
cd backend
pip install -r requirements.txt
```

**2. "API key not found" error**
- Make sure your `.env` file exists in the `backend/` directory
- Check that the API key is valid and has proper permissions
- Verify the `.env` file format is correct

**3. "Connection refused" error (Frontend)**
- Make sure the backend is running on port 5000
- Check that the API URL in `frontend/js/app.js` is correct
- Verify both servers are running simultaneously

**4. CORS errors**
- The backend includes CORS configuration for common frontend ports
- If using a different port, update the CORS settings in `backend/config.py`

**5. Port already in use**
- Backend: Change the port in `backend/app.py` or kill the process using port 5000
- Frontend: Use a different port: `python -m http.server 8081`

### File Upload Issues

- Supported file types: PDF, TXT, DOCX
- Maximum file size: 16MB
- Make sure files are not corrupted or password-protected

### API Rate Limits

OpenRouter has rate limits on API calls. If you hit limits:
- Wait a few minutes before making more requests
- Consider upgrading your OpenRouter plan
- Implement caching for repeated requests

## Development Workflow

### Backend Development
```bash
cd backend
python app.py
```
- The server will auto-reload when you make changes to Python files
- Check the terminal for error messages and logs

### Frontend Development
```bash
cd frontend
python -m http.server 8080
```
- Edit HTML, CSS, or JavaScript files
- Refresh the browser to see changes
- Use browser developer tools (F12) for debugging

### Testing API Endpoints
You can test the backend API directly:

```bash
# Health check
curl http://localhost:5000/api/health

# Test with sample data
curl -X POST http://localhost:5000/api/analyze_text \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test legal document."}'
```

## Production Deployment

### Backend Production
1. Set `DEBUG=False` in your `.env` file
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. Set up a reverse proxy (nginx/Apache)
4. Use HTTPS with SSL certificates
5. Configure proper CORS origins for your domain

### Frontend Production
1. Update the API URL in `frontend/js/app.js` to point to your production backend
2. Deploy the `frontend/` directory to any static hosting service:
   - Netlify
   - Vercel
   - GitHub Pages
   - AWS S3
   - Any web server

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Consider implementing user authentication for production use
- Monitor API usage to avoid unexpected charges
- Use HTTPS in production

## Support

If you encounter issues:

1. **Backend Issues**: Check the Flask server logs in the terminal
2. **Frontend Issues**: Open browser developer tools (F12) and check the console
3. **API Issues**: Verify your OpenRouter API key is working
4. **Connection Issues**: Ensure both servers are running and ports are correct

For additional help:
- Backend documentation: `backend/README.md`
- Frontend documentation: `frontend/README.md`
- Main project documentation: `README.md`
