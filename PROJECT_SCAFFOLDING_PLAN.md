# Yasashii Sensei - Complete Project Scaffolding Plan

**Purpose**: Detailed plan for creating the complete project structure before implementation begins.

**Critical Note**: Telegram bot is a CORE REQUIRED MVP feature, not a stretch goal.

---

## 1. Complete Directory Structure

```
yasashii-sensei/
├── .bob/                              # AI assistant mode-specific rules
│   ├── rules-code/
│   │   └── AGENTS.md                  # Code mode rules
│   ├── rules-advanced/
│   │   └── AGENTS.md                  # Advanced mode rules
│   ├── rules-ask/
│   │   └── AGENTS.md                  # Ask mode rules
│   └── rules-plan/
│       └── AGENTS.md                  # Plan mode rules
│
├── config/                            # Configuration and prompts
│   ├── __init__.py                    # Empty init file
│   └── prompts.py                     # ALL watsonx.ai prompts (CRITICAL)
│
├── services/                          # Business logic services
│   ├── __init__.py                    # Empty init file
│   ├── watsonx_service.py             # watsonx.ai API integration
│   ├── articles_service.py            # Hardcoded sample articles
│   └── telegram_service.py            # Telegram bot (CORE MVP)
│
├── utils/                             # Utility functions
│   ├── __init__.py                    # Empty init file
│   ├── cache.py                       # Simple in-memory TTL cache
│   └── text_processor.py              # Japanese text utilities
│
├── static/                            # Static web assets
│   ├── css/
│   │   └── style.css                  # Main stylesheet
│   ├── js/
│   │   └── app.js                     # Frontend JavaScript
│   └── images/
│       └── logo.png                   # App logo (placeholder)
│
├── templates/                         # Jinja2 HTML templates
│   ├── base.html                      # Base template with common elements
│   ├── index.html                     # Homepage (text input + article browser)
│   └── results.html                   # Analysis results display
│
├── tests/                             # Optional tests (manual testing priority)
│   ├── __init__.py                    # Empty init file
│   ├── test_watsonx.py                # watsonx.ai integration tests
│   └── test_articles.py               # Sample articles tests
│
├── app.py                             # Main Flask application (ALL routes)
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variable template
├── .env                               # Actual environment variables (gitignored)
├── .gitignore                         # Git ignore patterns
├── README.md                          # Project documentation
├── AGENTS.md                          # General AI assistant guidance
├── YASASHII_SENSEI_BOB_BRIEF.md      # Complete technical specification
└── PROJECT_SCAFFOLDING_PLAN.md       # This file
```

---

## 2. File Creation Order and Dependencies

### Phase 1: Foundation Files (No Dependencies)

**Order 1: Git and Environment Setup**
1. `.gitignore` - Define what to ignore
2. `.env.example` - Environment variable template
3. `README.md` - Project overview (already exists, may need update)

**Order 2: AI Assistant Rules**
4. `.bob/rules-code/AGENTS.md` - Move from `.bob-rules-code-AGENTS.md`
5. `.bob/rules-advanced/AGENTS.md` - Move from `.bob-rules-advanced-AGENTS.md`
6. `.bob/rules-ask/AGENTS.md` - Move from `.bob-rules-ask-AGENTS.md`
7. `.bob/rules-plan/AGENTS.md` - Move from `.bob-rules-plan-AGENTS.md`

**Order 3: Python Package Structure**
8. `config/__init__.py` - Empty file
9. `services/__init__.py` - Empty file
10. `utils/__init__.py` - Empty file
11. `tests/__init__.py` - Empty file

### Phase 2: Configuration and Utilities (Foundation Dependencies)

**Order 4: Core Configuration**
12. `config/prompts.py` - AI prompts and model configuration (CRITICAL)
13. `requirements.txt` - Python dependencies

**Order 5: Utility Modules**
14. `utils/cache.py` - Simple in-memory cache with TTL
15. `utils/text_processor.py` - Japanese text utilities

### Phase 3: Service Layer (Config + Utils Dependencies)

**Order 6: Service Integrations**
16. `services/watsonx_service.py` - watsonx.ai integration (depends on config/prompts.py)
17. `services/articles_service.py` - Hardcoded sample articles (no dependencies)
18. `services/telegram_service.py` - Telegram bot (CORE MVP, depends on watsonx_service.py)

### Phase 4: Web Application (All Service Dependencies)

**Order 7: Flask Application**
19. `app.py` - Main Flask app with all routes (depends on all services)

### Phase 5: Frontend Assets (Can be parallel with backend)

**Order 8: Templates**
20. `templates/base.html` - Base template
21. `templates/index.html` - Homepage
22. `templates/results.html` - Results page

**Order 9: Static Assets**
23. `static/css/style.css` - Stylesheet
24. `static/js/app.js` - Frontend JavaScript
25. `static/images/logo.png` - Placeholder logo

### Phase 6: Testing (Optional, after core implementation)

**Order 10: Test Files**
26. `tests/test_watsonx.py` - watsonx.ai tests
27. `tests/test_articles.py` - Sample articles tests

---

## 3. Detailed File Specifications

### 3.1 Configuration Files

#### `.gitignore`
```
# Environment
.env
venv/
env/
__pycache__/
*.pyc

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

#### `.env.example`
```bash
# IBM watsonx.ai Configuration
WATSONX_API_KEY=
WATSONX_PROJECT_ID=
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PRIMARY_MODEL=ibm/granite-4-h-small
WATSONX_FALLBACK_MODEL=meta-llama/llama-3-3-70b-instruct

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=change_this_to_random_string

# Sample Articles (no external API needed)
# NHK Web Easy requires authentication - using hardcoded samples instead

# Telegram Bot (REQUIRED - Core MVP Feature)
TELEGRAM_BOT_TOKEN=
TELEGRAM_WEBHOOK_URL=

# Application Settings
MAX_TEXT_LENGTH=5000
DEFAULT_JLPT_LEVEL=N4
ENABLE_CULTURAL_NOTES=true
ENABLE_COMPREHENSION_QUESTIONS=true
```

#### `requirements.txt`
```
flask==3.0.0
python-dotenv==1.0.0
ibm-watsonx-ai>=1.0.0
python-telegram-bot==20.7
gunicorn==21.2.0
```

### 3.2 Core Python Modules

#### `config/prompts.py`
**Purpose**: Centralize ALL AI prompts and model configuration
**Key Contents**:
- Model constants: PRIMARY_MODEL, FALLBACK_MODEL, BANNED_MODELS
- SYSTEM_CONTEXT prompt
- COMBINED_ANALYSIS_PROMPT (main prompt for MVP)
- MODEL_PARAMS (temperature, tokens, etc.)

#### `utils/cache.py`
**Purpose**: Simple in-memory cache with TTL
**Key Functions**:
- `set(key, value, ttl)` - Store with expiration
- `get(key)` - Retrieve if not expired
- `clear()` - Clear all cache
- `is_expired(key)` - Check expiration

#### `utils/text_processor.py`
**Purpose**: Japanese text utilities
**Key Functions**:
- `count_characters(text)` - Count Japanese characters
- `has_japanese(text)` - Validate Japanese content
- `truncate_text(text, max_length)` - Truncate safely

#### `services/watsonx_service.py`
**Purpose**: watsonx.ai API integration
**Key Class**: `WatsonxService`
**Key Methods**:
- `__init__(api_key, project_id)` - Initialize with credentials
- `analyze_text(japanese_text)` - Main analysis method
- `_switch_to_fallback()` - Switch to fallback model
- `_extract_json(text)` - Parse JSON from response

#### `services/articles_service.py`
**Purpose**: Hardcoded sample Japanese articles
**Key Contents**:
- `SAMPLE_ARTICLES` - List of 5 curated articles
- Each article has: id, title, content, date, difficulty (N5-N2), topic
- `get_articles()` - Return all sample articles
- `get_article_by_id(article_id)` - Get specific article
- No caching needed (articles are constants)

**Sample Article Structure**:
```python
{
    "id": "article_001",
    "title": "東京で新しい美術館がオープン",
    "content": "東京の上野に新しい美術館がオープンしました。この美術館では、日本の伝統的な芸術作品と現代アートの両方を見ることができます。入場料は大人1000円、子供500円です。",
    "date": "2026-05-15",
    "difficulty": "N4",
    "topic": "culture"
}
```

#### `services/telegram_service.py` (CORE MVP)
**Purpose**: Telegram bot integration
**Key Class**: `TelegramService`
**Key Methods**:
- `__init__(bot_token, watsonx_service, articles_service)` - Initialize bot
- `start_command(update, context)` - Handle /start
- `help_command(update, context)` - Handle /help
- `articles_command(update, context)` - Handle /articles (show Today's Articles)
- `handle_message(update, context)` - Handle text messages
- `format_analysis_for_telegram(analysis)` - Format response

#### `app.py`
**Purpose**: Main Flask application with ALL routes
**Key Routes**:
- `GET /` - Homepage
- `POST /api/analyze` - Analyze Japanese text
- `GET /api/articles` - Get sample articles
- `GET /api/articles/<id>` - Get specific article
- `GET /api/health` - Health check
- `POST /api/telegram/webhook` - Telegram webhook

### 3.3 Frontend Files

#### `templates/base.html`
**Purpose**: Base template with common HTML structure
**Key Elements**:
- HTML5 doctype and meta tags
- Google Fonts (Noto Sans JP)
- CSS link to style.css
- JavaScript link to app.js
- Block for page-specific content

#### `templates/index.html`
**Purpose**: Homepage with text input and NHK browser
**Key Elements**:
- Text input textarea
- "Analyze with AI" button
- "Browse NHK Web Easy" button
- Loading spinner
- Quick example buttons

#### `templates/results.html`
**Purpose**: Display analysis results
**Key Elements**:
- Original text display
- JLPT level badge
- Vocabulary section (expandable)
- Grammar section (expandable)
- Translation section
- Cultural notes section (if enabled)
- "Analyze Another" button

#### `static/css/style.css`
**Purpose**: Main stylesheet
**Key Styles**:
- CSS variables for colors
- Typography (Noto Sans JP)
- Layout (flexbox/grid)
- Component styles (buttons, cards, badges)
- Responsive breakpoints
- Loading animations

#### `static/js/app.js`
**Purpose**: Frontend JavaScript
**Key Functions**:
- `analyzeText()` - Submit text for analysis
- `loadNHKArticles()` - Fetch and display NHK articles
- `selectArticle(articleId)` - Load article into textarea
- `displayResults(data)` - Render analysis results
- `showLoading()` / `hideLoading()` - Loading states

---

## 4. Scaffolding Execution Strategy

### Strategy A: Sequential Creation (Recommended for Code Mode)

**Advantages**:
- Clear dependency order
- Test each component as you build
- Easier to debug issues

**Execution**:
1. Create all directories first
2. Create files in dependency order (Phase 1 → Phase 6)
3. Test each service module independently
4. Integrate into Flask app
5. Build frontend last

### Strategy B: Parallel Creation (For Multiple Developers)

**Advantages**:
- Faster overall completion
- Team can work simultaneously

**Execution**:
- Developer 1: Backend (config, services, app.py)
- Developer 2: Frontend (templates, static assets)
- Developer 3: Telegram bot (telegram_service.py)

### Strategy C: Vertical Slice (For Rapid Prototyping)

**Advantages**:
- End-to-end functionality quickly
- Early validation of architecture

**Execution**:
1. Minimal app.py with one route
2. Basic watsonx_service.py
3. Simple index.html
4. Expand incrementally

---

## 5. Critical Implementation Notes

### 5.1 Telegram Bot (CORE MVP)

**CRITICAL**: Telegram bot is NOT optional. It must be implemented as part of core MVP.

**Implementation Priority**: Phase 2 (Hours 16-20)

**Key Requirements**:
- Share same Flask backend as web app
- Use same watsonx_service.py for analysis
- Format responses for Telegram markdown
- Implement commands: /start, /help, /nhk
- Handle direct text messages for analysis

### 5.2 Model Configuration

**CRITICAL**: Never use `mistral-medium-2505` - it's banned for this hackathon.

**Model Setup**:
- Primary: `ibm/granite-4-h-small` (fast, optimized)
- Fallback: `meta-llama/llama-3-3-70b-instruct`
- All model IDs in `config/prompts.py`

### 5.3 No Database

**CRITICAL**: Use in-memory caching only. No database setup.

**Caching Strategy**:
- NHK articles: 1-hour TTL
- Store in Python dict with timestamps
- Clear expired entries on access

### 5.4 Prompt Engineering

**CRITICAL**: Use combined prompt to reduce API calls.

**Prompt Requirements**:
- Request JSON-only responses
- Include all analysis types in one prompt
- Handle non-JSON responses gracefully

---

## 6. Validation Checklist

Before starting implementation, verify:

- [ ] All directories planned
- [ ] All files identified with purpose
- [ ] Dependencies mapped correctly
- [ ] Telegram bot included as CORE MVP
- [ ] Model configuration correct (granite-4-h-small primary)
- [ ] No database dependencies
- [ ] Environment variables documented
- [ ] File creation order logical

---

## 7. Next Steps

1. **Review this plan** with team/stakeholders
2. **Choose execution strategy** (Sequential recommended)
3. **Switch to Code mode** to begin implementation
4. **Create directories first** (all at once)
5. **Create files in order** (Phase 1 → Phase 6)
6. **Test incrementally** as you build
7. **Follow 48-hour build plan** from technical brief

---

## 8. Success Criteria

Project scaffolding is complete when:

✅ All directories exist  
✅ All configuration files created  
✅ All Python modules created with proper structure  
✅ All templates created  
✅ All static assets created  
✅ Dependencies installed (`pip install -r requirements.txt`)  
✅ Environment variables configured (`.env` from `.env.example`)  
✅ Telegram bot token obtained from BotFather  
✅ watsonx.ai credentials configured  
✅ Project can be run (`python app.py`)  

Ready to implement! 🚀