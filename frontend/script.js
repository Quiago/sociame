/**
 * Community Manager Assistant MVP - Frontend JavaScript
 * Handles UI interactions and API communication
 */

// ===== Configuration =====
const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINTS = {
    generateContent: `${API_BASE_URL}/api/generate-content`,
    guidedQuestions: `${API_BASE_URL}/api/guided-questions`
};

// ===== Global State =====
let currentTab = 'text';
let isGenerating = false;

// ===== DOM Elements =====
const elements = {
    // Tabs
    tabButtons: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),
    
    // Inputs
    textInput: document.getElementById('text-input'),
    urlInput: document.getElementById('url-input'),
    imageInput: document.getElementById('image-input'),
    imagePreview: document.getElementById('image-preview'),
    nicheInput: document.getElementById('niche-input'),
    objectiveSelect: document.getElementById('objective-select'),
    toneSelect: document.getElementById('tone-select'),
    
    // Buttons
    generateBtn: document.getElementById('generate-btn'),
    newGenerationBtn: document.getElementById('new-generation-btn'),
    retryBtn: document.getElementById('retry-btn'),
    
    // Sections
    inputSection: document.querySelector('.input-section'),
    loadingSection: document.getElementById('loading-section'),
    resultsSection: document.getElementById('results-section'),
    errorSection: document.getElementById('error-section'),
    
    // Results containers
    contextText: document.getElementById('context-text'),
    ideasContainer: document.getElementById('ideas-container'),
    postsContainer: document.getElementById('posts-container'),
    visualsContainer: document.getElementById('visuals-container'),
    errorText: document.getElementById('error-text')
};

// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    setupFileUpload();
});

function initializeEventListeners() {
    // Tab switching
    elements.tabButtons.forEach(button => {
        button.addEventListener('click', () => switchTab(button.dataset.tab));
    });
    
    // Generate button
    elements.generateBtn.addEventListener('click', handleGenerate);
    
    // New generation button
    elements.newGenerationBtn.addEventListener('click', resetToInput);
    
    // Retry button
    elements.retryBtn.addEventListener('click', handleGenerate);
    
    // Enter key support
    document.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isGenerating) {
            if (e.target.matches('input, textarea, select')) {
                handleGenerate();
            }
        }
    });
}

function setupFileUpload() {
    const fileUpload = document.querySelector('.file-upload');
    const fileInput = elements.imageInput;
    
    // Click to upload
    fileUpload.addEventListener('click', () => fileInput.click());
    
    // Drag and drop
    fileUpload.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUpload.style.borderColor = '#667eea';
        fileUpload.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
    });
    
    fileUpload.addEventListener('dragleave', (e) => {
        e.preventDefault();
        fileUpload.style.borderColor = '#e0e0e0';
        fileUpload.style.backgroundColor = 'transparent';
    });
    
    fileUpload.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUpload.style.borderColor = '#e0e0e0';
        fileUpload.style.backgroundColor = 'transparent';
        
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].type.startsWith('image/')) {
            fileInput.files = files;
            previewImage(files[0]);
        }
    });
    
    // File selection
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            previewImage(e.target.files[0]);
        }
    });
}

// ===== Tab Management =====
function switchTab(tabName) {
    currentTab = tabName;
    
    // Update tab buttons
    elements.tabButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    
    // Update tab contents
    elements.tabContents.forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });
    
    // Clear previous inputs when switching tabs
    clearInputs();
}

function clearInputs() {
    elements.textInput.value = '';
    elements.urlInput.value = '';
    elements.imageInput.value = '';
    elements.nicheInput.value = '';
    elements.objectiveSelect.value = '';
    elements.toneSelect.value = '';
    elements.imagePreview.classList.add('hidden');
}

// ===== Image Preview =====
function previewImage(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        elements.imagePreview.innerHTML = `
            <img src="${e.target.result}" alt="Preview">
            <p>Imagen seleccionada: ${file.name}</p>
        `;
        elements.imagePreview.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
}

// ===== Content Generation =====
async function handleGenerate() {
    if (isGenerating) return;
    
    try {
        // Validate input
        const validation = validateInput();
        if (!validation.isValid) {
            showError(validation.message);
            return;
        }
        
        // Show loading
        showLoading();
        
        // Prepare form data
        const formData = await prepareFormData();
        
        // Call API
        const response = await fetch(API_ENDPOINTS.generateContent, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error del servidor');
        }
        
        const data = await response.json();
        
        // Show results
        showResults(data);
        
    } catch (error) {
        console.error('Error generating content:', error);
        showError(error.message || 'Error inesperado. Por favor, intenta de nuevo.');
    }
}

function validateInput() {
    switch (currentTab) {
        case 'text':
            if (!elements.textInput.value.trim()) {
                return { isValid: false, message: 'Por favor, ingresa un texto o tema.' };
            }
            break;
        
        case 'url':
            if (!elements.urlInput.value.trim()) {
                return { isValid: false, message: 'Por favor, ingresa una URL.' };
            }
            if (!isValidUrl(elements.urlInput.value)) {
                return { isValid: false, message: 'Por favor, ingresa una URL válida.' };
            }
            break;
        
        case 'image':
            if (!elements.imageInput.files.length) {
                return { isValid: false, message: 'Por favor, selecciona una imagen.' };
            }
            break;
        
        case 'guided':
            if (!elements.nicheInput.value.trim() || 
                !elements.objectiveSelect.value || 
                !elements.toneSelect.value) {
                return { isValid: false, message: 'Por favor, completa todos los campos del formulario guiado.' };
            }
            break;
    }
    
    return { isValid: true };
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

async function prepareFormData() {
    const formData = new FormData();
    formData.append('input_type', currentTab);
    
    switch (currentTab) {
        case 'text':
            formData.append('content', elements.textInput.value.trim());
            break;
        
        case 'url':
            formData.append('content', elements.urlInput.value.trim());
            break;
        
        case 'image':
            formData.append('image', elements.imageInput.files[0]);
            break;
        
        case 'guided':
            const guidedAnswers = {
                niche: elements.nicheInput.value.trim(),
                objective: elements.objectiveSelect.value,
                tone: elements.toneSelect.value
            };
            formData.append('guided_answers', JSON.stringify(guidedAnswers));
            break;
    }
    
    return formData;
}

// ===== UI State Management =====
function showLoading() {
    isGenerating = true;
    elements.generateBtn.disabled = true;
    elements.generateBtn.textContent = 'Generando...';
    
    elements.inputSection.classList.add('hidden');
    elements.resultsSection.classList.add('hidden');
    elements.errorSection.classList.add('hidden');
    elements.loadingSection.classList.remove('hidden');
}

function showResults(data) {
    isGenerating = false;
    elements.generateBtn.disabled = false;
    elements.generateBtn.textContent = '✨ Generar Contenido';
    
    elements.loadingSection.classList.add('hidden');
    elements.errorSection.classList.add('hidden');
    elements.resultsSection.classList.remove('hidden', 'fade-in');
    
    // Populate results
    populateResults(data);
    
    // Scroll to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    isGenerating = false;
    elements.generateBtn.disabled = false;
    elements.generateBtn.textContent = '✨ Generar Contenido';
    
    elements.loadingSection.classList.add('hidden');
    elements.resultsSection.classList.add('hidden');
    elements.errorSection.classList.remove('hidden');
    
    elements.errorText.textContent = message;
    
    // Scroll to error
    elements.errorSection.scrollIntoView({ behavior: 'smooth' });
}

function resetToInput() {
    elements.resultsSection.classList.add('hidden');
    elements.errorSection.classList.add('hidden');
    elements.inputSection.classList.remove('hidden');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== Results Population =====
function populateResults(data) {
    // Context summary
    elements.contextText.textContent = data.context_summary;
    
    // Ideas
    populateIdeas(data.ideas);
    
    // Posts
    populatePosts(data.posts);
    
    // Visual prompts
    populateVisualPrompts(data.visual_prompts);
}

function populateIdeas(ideas) {
    elements.ideasContainer.innerHTML = '';
    
    ideas.forEach((idea, index) => {
        const ideaCard = document.createElement('div');
        ideaCard.className = 'idea-card';
        ideaCard.innerHTML = `
            <h4>💡 ${idea.title}</h4>
            <p>${idea.description}</p>
        `;
        elements.ideasContainer.appendChild(ideaCard);
    });
}

function populatePosts(posts) {
    elements.postsContainer.innerHTML = '';
    
    posts.forEach((post, index) => {
        const postCard = document.createElement('div');
        postCard.className = 'instagram-post-card';
        
        const hashtags = Array.isArray(post.hashtags) ? post.hashtags : [];
        
        postCard.innerHTML = `
            <div class="instagram-post">
                <div class="instagram-header">
                    <div class="instagram-profile">
                        <div class="profile-pic">✨</div>
                        <div class="profile-info">
                            <div class="username">@content_creator</div>
                            <div class="location">Creando contenido 📍</div>
                        </div>
                    </div>
                    <div class="instagram-menu">⋯</div>
                </div>
                
                <div class="instagram-image">
                    <div class="placeholder-image">
                        📸 Imagen generada aquí
                        <small>Usa el prompt visual correspondiente de la sección "Prompts para imágenes"</small>
                    </div>
                </div>
                
                <div class="instagram-actions">
                    <div class="action-buttons">
                        <span class="action-btn">❤️</span>
                        <span class="action-btn">💬</span>
                        <span class="action-btn">📤</span>
                    </div>
                    <div class="bookmark">🔖</div>
                </div>
                
                <div class="instagram-likes">
                    <strong>1,234 Me gusta</strong>
                </div>
                
                <div class="instagram-caption">
                    <div class="caption-text">
                        <strong>@content_creator</strong> ${post.hook}
                        <br><br>
                        ${post.body}
                        <br><br>
                        ${post.cta}
                        <br><br>
                        <span class="hashtags-text">
                            ${hashtags.join(' ')}
                        </span>
                    </div>
                </div>
                
                <div class="instagram-comments">
                    <div class="comment">
                        <strong>@usuario_fan</strong> ¡Increíble contenido! 😍
                    </div>
                    <div class="comment">
                        <strong>@seguidor_activo</strong> ¡Excelente post! 👏
                    </div>
                    <div class="view-comments">Ver los 47 comentarios</div>
                </div>
                
                <div class="instagram-time">
                    hace 2 horas
                </div>
            </div>
        `;
        
        elements.postsContainer.appendChild(postCard);
    });
}

function populateVisualPrompts(visualPrompts) {
    elements.visualsContainer.innerHTML = '';
    
    visualPrompts.forEach((visual, index) => {
        const visualCard = document.createElement('div');
        visualCard.className = 'visual-card';
        visualCard.innerHTML = `
            <h4>🎨 Prompt para imagen ${index + 1}</h4>
            <div class="visual-prompt">
                "${visual.description}"
            </div>
        `;
        elements.visualsContainer.appendChild(visualCard);
    });
}

// ===== Utility Functions =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== Analytics and Error Tracking =====
function trackEvent(eventName, eventData = {}) {
    // Simple console logging for MVP
    // In production, integrate with analytics service
    console.log('Event:', eventName, eventData);
}

function trackError(error, context = {}) {
    // Simple error logging for MVP
    // In production, integrate with error reporting service
    console.error('Error:', error, context);
}

// ===== Service Worker Registration (Future Enhancement) =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Service worker for offline functionality
        // navigator.serviceWorker.register('/sw.js');
    });
}

// ===== Export for testing =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        switchTab,
        validateInput,
        isValidUrl,
        populateResults
    };
}