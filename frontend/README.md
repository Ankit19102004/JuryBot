# JuryBot Frontend

This is the frontend application for the JuryBot legal document translator.

## Features

- **Modern UI**: Beautiful, responsive design with glassmorphism effects
- **Document Upload**: Drag & drop file upload with support for PDF, TXT, DOC, DOCX
- **Text Analysis**: Paste legal text directly for instant analysis
- **Interactive Q&A**: Ask specific questions about uploaded documents
- **Clause Explanation**: Get detailed explanations of specific clauses
- **Real-time Feedback**: Loading states and progress indicators
- **Mobile Responsive**: Works perfectly on all device sizes

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **Vanilla JavaScript**: No frameworks, pure JavaScript
- **Font Awesome**: Icons
- **Google Fonts**: Inter font family

## File Structure

```
frontend/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # All styles and animations
├── js/
│   └── app.js          # Application logic
└── README.md           # This file
```

## Setup

1. **No build process required** - This is a static HTML/CSS/JS application
2. **Serve the files** using any web server:
   - Live Server (VS Code extension)
   - Python: `python -m http.server 8080`
   - Node.js: `npx serve .`
   - Any web server of your choice

3. **Open in browser**: Navigate to the served URL (usually `http://localhost:8080`)

## API Configuration

The frontend communicates with the backend API. Make sure to:

1. **Start the backend server** first (see backend README)
2. **Update API URL** in `js/app.js` if needed:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000/api';
   ```

## Development

### Local Development Server

Using Python (if installed):
```bash
cd frontend
python -m http.server 8080
```

Using Node.js (if installed):
```bash
cd frontend
npx serve .
```

Using Live Server (VS Code):
1. Install the "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Making Changes

- **HTML**: Edit `index.html` for structure changes
- **CSS**: Edit `css/style.css` for styling changes
- **JavaScript**: Edit `js/app.js` for functionality changes

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Features in Detail

### Document Upload
- Drag and drop interface
- File type validation
- Size limit enforcement (16MB)
- Visual feedback during upload

### Text Analysis
- Large textarea for pasting documents
- Character count validation
- Real-time analysis

### Results Display
- Summary card with document overview
- Risks and red flags identification
- Key terms and conditions extraction
- Actionable recommendations

### Interactive Features
- Question answering with context awareness
- Clause explanation with detailed breakdown
- Persistent document context across interactions

## Customization

### Styling
The application uses CSS custom properties for easy theming:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --text-color: #333;
    --background-color: #f8f9fa;
}
```

### API Endpoints
All API calls are centralized in `js/app.js`:

- `POST /api/upload` - File upload
- `POST /api/analyze_text` - Text analysis
- `POST /api/ask_question` - Question answering
- `POST /api/explain_clause` - Clause explanation

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the backend is running and CORS is properly configured
2. **API Connection**: Verify the API_BASE_URL in `js/app.js` matches your backend
3. **File Upload**: Check browser console for file size or type errors
4. **Styling Issues**: Clear browser cache if CSS changes aren't reflecting

### Debug Mode

Open browser developer tools (F12) to see:
- Network requests to the API
- JavaScript console errors
- Performance metrics

## Production Deployment

For production:

1. **Update API URL** to your production backend
2. **Minify assets** (optional but recommended)
3. **Enable compression** on your web server
4. **Set up HTTPS** for security
5. **Configure caching** headers appropriately

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see main project README for details
