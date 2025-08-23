// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

const uploadForm = document.getElementById('uploadForm');
const textForm = document.getElementById('textForm');
const questionForm = document.getElementById('questionForm');
const clauseForm = document.getElementById('clauseForm');

const fileInput = document.getElementById('fileInput');
const textInput = document.getElementById('textInput');
const questionInput = document.getElementById('questionInput');
const clauseInput = document.getElementById('clauseInput');

const questionAnswer = document.getElementById('questionAnswer');
const clauseExplanation = document.getElementById('clauseExplanation');
const answerText = document.getElementById('answerText');
const explanationText = document.getElementById('explanationText');

// Global variable to store current document text
let currentDocumentText = '';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    setupFileUpload();
    setupFormSubmissions();
    setupDragAndDrop();
    
    // Add fade-in animation to main content
    document.querySelector('.main').classList.add('fade-in');
}

function setupFileUpload() {
    // File input change handler
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            updateFileLabel(file.name);
        }
    });
}

function setupFormSubmissions() {
    // File upload form
    uploadForm.addEventListener('submit', handleFileUpload);
    
    // Text analysis form
    textForm.addEventListener('submit', handleTextAnalysis);
    
    // Question form
    questionForm.addEventListener('submit', handleQuestion);
    
    // Clause explanation form
    clauseForm.addEventListener('submit', handleClauseExplanation);
}

function setupDragAndDrop() {
    const fileLabel = document.querySelector('.file-input-label');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileLabel.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        fileLabel.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        fileLabel.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight(e) {
        fileLabel.classList.add('drag-over');
    }
    
    function unhighlight(e) {
        fileLabel.classList.remove('drag-over');
    }
    
    fileLabel.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            updateFileLabel(files[0].name);
        }
    }
}

function updateFileLabel(fileName) {
    const label = document.querySelector('.file-input-label span');
    label.textContent = fileName;
    
    const icon = document.querySelector('.file-input-label i');
    icon.className = 'fas fa-file-alt';
}

async function handleFileUpload(e) {
    e.preventDefault();
    
    const formData = new FormData(uploadForm);
    const file = formData.get('file');
    
    if (!file || file.size === 0) {
        showError('Please select a file to upload.');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) { // 16MB limit
        showError('File size must be less than 16MB.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store document text for future questions
            currentDocumentText = data.document_text || '';
            showResults(data.analysis);
        } else {
            showError(data.error || 'Upload failed. Please try again.');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showError('Network error. Please check your connection and try again.');
    }
}

async function handleTextAnalysis(e) {
    e.preventDefault();
    
    const text = textInput.value.trim();
    
    if (text.length < 10) {
        showError('Please enter at least 10 characters of text to analyze.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze_text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store document text for future questions
            currentDocumentText = text;
            showResults(data.analysis);
        } else {
            showError(data.error || 'Analysis failed. Please try again.');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        showError('Network error. Please check your connection and try again.');
    }
}

async function handleQuestion(e) {
    e.preventDefault();
    
    const question = questionInput.value.trim();
    
    if (!question) {
        showError('Please enter a question.');
        return;
    }
    
    if (!currentDocumentText) {
        showError('No document loaded. Please upload or paste a document first.');
        return;
    }
    
    // Show loading state for question
    const submitBtn = questionForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Asking...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/ask_question`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                question: question,
                document_text: currentDocumentText
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showQuestionAnswer(data.answer, question);
        } else {
            showError(data.error || 'Failed to get answer. Please try again.');
        }
    } catch (error) {
        console.error('Question error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        // Reset button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

async function handleClauseExplanation(e) {
    e.preventDefault();
    
    const clause = clauseInput.value.trim();
    
    if (!clause) {
        showError('Please enter a clause to explain.');
        return;
    }
    
    if (!currentDocumentText) {
        showError('No document loaded. Please upload or paste a document first.');
        return;
    }
    
    // Show loading state for clause explanation
    const submitBtn = clauseForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Explaining...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/explain_clause`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                clause: clause,
                document_text: currentDocumentText
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showClauseExplanation(data.explanation, clause);
        } else {
            showError(data.error || 'Failed to explain clause. Please try again.');
        }
    } catch (error) {
        console.error('Clause explanation error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        // Reset button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

function showLoading() {
    uploadSection.style.display = 'none';
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showResults(analysis) {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Populate results
    document.getElementById('summaryText').textContent = analysis.summary || 'No summary available.';
    
    // Populate risks
    const risksList = document.getElementById('risksList');
    risksList.innerHTML = '';
    if (analysis.risks && analysis.risks.length > 0) {
        analysis.risks.forEach(risk => {
            const li = document.createElement('li');
            li.textContent = risk;
            risksList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No significant risks identified.';
        li.style.color = '#28a745';
        risksList.appendChild(li);
    }
    
    // Populate terms
    const termsList = document.getElementById('termsList');
    termsList.innerHTML = '';
    if (analysis.terms && analysis.terms.length > 0) {
        analysis.terms.forEach(term => {
            const li = document.createElement('li');
            li.textContent = term;
            termsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No key terms identified.';
        termsList.appendChild(li);
    }
    
    // Populate recommendations
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';
    if (analysis.recommendations && analysis.recommendations.length > 0) {
        analysis.recommendations.forEach(recommendation => {
            const li = document.createElement('li');
            li.textContent = recommendation;
            recommendationsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No specific recommendations available.';
        recommendationsList.appendChild(li);
    }
    
    // Add fade-in animation
    resultsSection.classList.add('fade-in');
    
    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

function showQuestionAnswer(answer, question) {
    answerText.textContent = answer;
    questionAnswer.style.display = 'block';
    questionAnswer.classList.add('fade-in');
    
    // Clear the input
    questionInput.value = '';
    
    // Scroll to answer
    questionAnswer.scrollIntoView({ behavior: 'smooth' });
}

function showClauseExplanation(explanation, clause) {
    explanationText.innerHTML = explanation.replace(/\n/g, '<br>');
    clauseExplanation.style.display = 'block';
    clauseExplanation.classList.add('fade-in');
    
    // Clear the input
    clauseInput.value = '';
    
    // Scroll to explanation
    clauseExplanation.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'block';
    
    document.getElementById('errorMessage').textContent = message;
    
    // Scroll to error
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

function resetApp() {
    // Reset all forms
    uploadForm.reset();
    textForm.reset();
    questionForm.reset();
    clauseForm.reset();
    
    // Reset file label
    const label = document.querySelector('.file-input-label span');
    label.textContent = 'Choose a file or drag it here';
    
    const icon = document.querySelector('.file-input-label i');
    icon.className = 'fas fa-cloud-upload-alt';
    
    // Clear stored document text
    currentDocumentText = '';
    
    // Hide all sections except upload
    uploadSection.style.display = 'block';
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Hide answer boxes
    questionAnswer.style.display = 'none';
    clauseExplanation.style.display = 'none';
    
    // Remove fade-in classes
    resultsSection.classList.remove('fade-in');
    questionAnswer.classList.remove('fade-in');
    clauseExplanation.classList.remove('fade-in');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Utility function to show notifications
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#dc3545' : '#667eea'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Add CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .notification button {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        margin-left: auto;
    }
    
    .notification button:hover {
        opacity: 0.8;
    }
`;
document.head.appendChild(notificationStyles);

// Add drag-over styles to CSS
const dragOverStyles = document.createElement('style');
dragOverStyles.textContent = `
    .file-input-label.drag-over {
        border-color: #667eea !important;
        background: #f0f4ff !important;
        transform: scale(1.02);
    }
`;
document.head.appendChild(dragOverStyles);
