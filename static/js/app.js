// ===================================
// Configuration
// ===================================
const API_BASE_URL = 'http://localhost:5001';

// ===================================
// State Management
// ===================================
let currentArticles = [];

// ===================================
// Initialization
// ===================================
document.addEventListener('DOMContentLoaded', () => {
    console.log('Yasashii Sensei app initialized');
    
    // Fetch articles on page load
    fetchArticles();
    
    // Setup event listeners
    setupEventListeners();
    
    // Check if we're on results page and have data
    if (window.location.pathname.includes('/results')) {
        loadResultsFromSession();
    }
});

// ===================================
// Event Listeners Setup
// ===================================
function setupEventListeners() {
    // Analyze button
    const analyzeBtn = document.getElementById('analyze-btn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', analyzeText);
    }
    
    // Textarea character counter
    const textarea = document.getElementById('japanese-text');
    if (textarea) {
        textarea.addEventListener('input', updateCharacterCount);
        // Initialize counter
        updateCharacterCount();
    }
    
    // Enter key in textarea (optional: Ctrl+Enter to analyze)
    if (textarea) {
        textarea.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                analyzeText();
            }
        });
    }
}

// ===================================
// Tab Switching
// ===================================
function switchTab(tabName) {
    console.log('Switching to tab:', tabName);
    
    // Update tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(btn => {
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Update tab content
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        if (content.id === `${tabName}-tab`) {
            content.classList.add('active');
        } else {
            content.classList.remove('active');
        }
    });
}

// ===================================
// Fetch Articles
// ===================================
async function fetchArticles() {
    console.log('Fetching articles...');
    const articlesContainer = document.getElementById('articles-list');
    
    if (!articlesContainer) {
        console.log('Articles container not found (not on homepage)');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/articles`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Articles fetched:', data);
        
        currentArticles = data.articles || [];
        displayArticles(currentArticles);
        
    } catch (error) {
        console.error('Error fetching articles:', error);
        articlesContainer.innerHTML = `
            <div class="error-message">
                Failed to load articles. Please refresh the page or try again later.
            </div>
        `;
    }
}

// ===================================
// Display Articles
// ===================================
function displayArticles(articles) {
    const articlesContainer = document.getElementById('articles-list');
    
    if (!articles || articles.length === 0) {
        articlesContainer.innerHTML = '<div class="loading-message">No articles available</div>';
        return;
    }
    
    articlesContainer.innerHTML = articles.map(article => `
        <div class="article-card" onclick="selectArticle('${article.id}')">
            <div class="article-card-header">
                <div>
                    <h3 class="article-title">${escapeHtml(article.title)}</h3>
                </div>
                <span class="jlpt-badge ${article.difficulty.toLowerCase()}">${article.difficulty}</span>
            </div>
            <div class="article-meta">
                <span class="article-topic">📌 ${escapeHtml(article.topic)}</span>
                <span class="article-date">📅 ${escapeHtml(article.date)}</span>
            </div>
        </div>
    `).join('');
}

// ===================================
// Select Article
// ===================================
function selectArticle(articleId) {
    console.log('Article selected:', articleId);
    
    const article = currentArticles.find(a => a.id === articleId);
    if (!article) {
        console.error('Article not found:', articleId);
        return;
    }
    
    // Load article content into textarea
    const textarea = document.getElementById('japanese-text');
    if (textarea) {
        textarea.value = article.content;
        updateCharacterCount();
    }
    
    // Switch to paste tab
    switchTab('paste');
    
    // Scroll to textarea
    textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// ===================================
// Update Character Count
// ===================================
function updateCharacterCount() {
    const textarea = document.getElementById('japanese-text');
    const charCount = document.getElementById('char-count');
    
    if (!textarea || !charCount) return;
    
    const count = textarea.value.length;
    charCount.textContent = count;
    
    // Warn if approaching limit
    if (count > 4500) {
        charCount.style.color = 'var(--n1-red)';
    } else if (count > 4000) {
        charCount.style.color = 'var(--n2-orange)';
    } else {
        charCount.style.color = 'var(--primary-navy)';
    }
}

// ===================================
// Analyze Text
// ===================================
async function analyzeText() {
    console.log('Analyzing text...');
    
    const textarea = document.getElementById('japanese-text');
    const text = textarea.value.trim();
    
    // Validation
    if (!text) {
        showError('Please enter some Japanese text to analyze.');
        return;
    }
    
    // Check for Japanese characters
    const hasJapanese = /[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]/.test(text);
    if (!hasJapanese) {
        showError('Please enter text containing Japanese characters (hiragana, katakana, or kanji).');
        textarea.classList.add('error');
        return;
    }
    
    // Check length
    if (text.length > 5000) {
        showError('Text is too long. Please limit to 5000 characters.');
        return;
    }
    
    // Clear any previous errors
    hideError();
    textarea.classList.remove('error');
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Analysis complete:', data);
        
        // Store results in sessionStorage for results page
        sessionStorage.setItem('analysisResults', JSON.stringify(data));
        sessionStorage.setItem('originalText', text);
        
        // Redirect to results page
        window.location.href = '/results';
        
    } catch (error) {
        console.error('Error analyzing text:', error);
        hideLoading();
        showError(`Analysis failed: ${error.message}. Please try again.`);
    }
}

// ===================================
// Load Results from Session
// ===================================
function loadResultsFromSession() {
    const resultsData = sessionStorage.getItem('analysisResults');
    const originalText = sessionStorage.getItem('originalText');
    
    if (resultsData && originalText) {
        try {
            const data = JSON.parse(resultsData);
            displayResults(data, originalText);
        } catch (error) {
            console.error('Error loading results:', error);
        }
    }
}

// ===================================
// Display Results
// ===================================
function displayResults(data, originalText) {
    console.log('Displaying results:', data);
    
    // Display original text with furigana
    displayOriginalText(originalText, data.vocabulary || []);
    
    // Display JLPT level badge
    displayJLPTBadge(data.jlpt_level || 'N3');
    
    // Display vocabulary
    displayVocabulary(data.vocabulary || []);
    
    // Display grammar patterns (API returns grammar_points, not grammar_patterns)
    displayGrammar(data.grammar_points || data.grammar_patterns || []);
    
    // Display translation
    displayTranslation(data.translation || '');
    
    // Display cultural notes
    displayCulturalNotes(data.cultural_notes || []);
}

// ===================================
// Display Original Text with Furigana
// ===================================
function displayOriginalText(text, vocabulary) {
    const container = document.getElementById('original-text-with-furigana');
    if (!container) return;
    
    // Simple approach: wrap text in paragraph
    // For MVP, we'll show plain text (furigana generation is complex)
    // In production, you'd use a library or backend service
    container.innerHTML = `<p>${escapeHtml(text)}</p>`;
}

// ===================================
// Display JLPT Level Badge
// ===================================
function displayJLPTBadge(level) {
    const badge = document.getElementById('jlpt-level-badge');
    if (!badge) return;
    
    const levelLower = level.toLowerCase();
    badge.className = `jlpt-badge ${levelLower}`;
    badge.textContent = level;
}

// ===================================
// Display Vocabulary
// ===================================
function displayVocabulary(vocabulary) {
    const container = document.getElementById('vocabulary-grid');
    if (!container) return;
    
    if (!vocabulary || vocabulary.length === 0) {
        container.innerHTML = '<p>No vocabulary items found.</p>';
        return;
    }
    
    container.innerHTML = vocabulary.map(item => `
        <div class="vocab-card">
            <div class="vocab-word">${escapeHtml(item.word || '')}</div>
            <div class="vocab-reading">${escapeHtml(item.reading || '')}</div>
            <div class="vocab-meaning">${escapeHtml(item.meaning || '')}</div>
            <span class="jlpt-badge ${(item.jlpt_level || 'n3').toLowerCase()}">${item.jlpt_level || 'N3'}</span>
        </div>
    `).join('');
}

// ===================================
// Display Grammar Patterns
// ===================================
function displayGrammar(patterns) {
    const container = document.getElementById('grammar-list');
    if (!container) return;
    
    if (!patterns || patterns.length === 0) {
        container.innerHTML = '<p>No grammar patterns identified.</p>';
        return;
    }
    
    container.innerHTML = patterns.map(pattern => `
        <div class="grammar-item">
            <div class="grammar-structure">${escapeHtml(pattern.pattern || '')}</div>
            <div class="grammar-explanation">${escapeHtml(pattern.explanation || '')}</div>
            ${pattern.example ? `<div class="grammar-example">${escapeHtml(pattern.example)}</div>` : ''}
            ${pattern.jlpt_level ? `<span class="jlpt-badge ${pattern.jlpt_level.toLowerCase()}">${pattern.jlpt_level}</span>` : ''}
        </div>
    `).join('');
}

// ===================================
// Display Translation
// ===================================
function displayTranslation(translation) {
    const container = document.getElementById('translation-text');
    if (!container) return;
    
    container.innerHTML = `<p>${escapeHtml(translation || 'Translation not available.')}</p>`;
}

// ===================================
// Display Cultural Notes
// ===================================
function displayCulturalNotes(notes) {
    const container = document.getElementById('cultural-notes-list');
    if (!container) return;
    
    if (!notes || notes.length === 0) {
        container.innerHTML = '<li>No cultural notes available.</li>';
        return;
    }
    
    container.innerHTML = notes.map(note => {
        // Handle both string and object formats
        if (typeof note === 'string') {
            return `<li>${escapeHtml(note)}</li>`;
        } else if (note && note.explanation) {
            // Extract explanation property from object
            const topic = note.topic ? `<strong>${escapeHtml(note.topic)}:</strong> ` : '';
            return `<li>${topic}${escapeHtml(note.explanation)}</li>`;
        }
        return '';
    }).join('');
}

// ===================================
// Text-to-Speech Function
// ===================================
async function listenToText() {
    console.log('Playing text-to-speech...');
    
    const button = document.getElementById('listen-btn');
    const originalText = sessionStorage.getItem('originalText');
    
    if (!originalText) {
        console.error('No original text found');
        return;
    }
    
    // Show loading state
    button.textContent = '⏳ Loading...';
    button.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/tts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: originalText })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        // Get audio blob
        const audioBlob = await response.blob();
        
        // Create audio URL
        const audioUrl = URL.createObjectURL(audioBlob);
        
        // Create and play audio
        const audio = new Audio(audioUrl);
        
        // Update button to show playing state
        button.textContent = '⏸ Playing...';
        
        // Play audio
        await audio.play();
        
        // Reset button when audio ends
        audio.addEventListener('ended', () => {
            button.textContent = '🔊 Listen';
            button.disabled = false;
            URL.revokeObjectURL(audioUrl);
        });
        
        // Handle errors during playback
        audio.addEventListener('error', (e) => {
            console.error('Audio playback error:', e);
            button.textContent = '🔊 Listen';
            button.disabled = false;
            URL.revokeObjectURL(audioUrl);
        });
        
    } catch (error) {
        console.error('Error playing audio:', error);
        button.textContent = '🔊 Listen';
        button.disabled = false;
        alert('Failed to play audio. Please try again.');
    }
}

// ===================================
// Loading State Management
// ===================================
function showLoading() {
    const spinner = document.getElementById('loading-spinner');
    const button = document.getElementById('analyze-btn');
    
    if (spinner) spinner.style.display = 'flex';
    if (button) button.disabled = true;
}

function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    const button = document.getElementById('analyze-btn');
    
    if (spinner) spinner.style.display = 'none';
    if (button) button.disabled = false;
}

// ===================================
// Error Message Management
// ===================================
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
}

function hideError() {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.style.display = 'none';
        errorDiv.textContent = '';
    }
}

// ===================================
// Utility Functions
// ===================================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===================================
// Make functions globally accessible
// ===================================
window.switchTab = switchTab;
window.selectArticle = selectArticle;
window.analyzeText = analyzeText;
window.listenToText = listenToText;

console.log('Yasashii Sensei app.js loaded successfully');

// Made with Bob
