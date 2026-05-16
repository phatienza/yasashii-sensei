# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project: Yasashii Sensei (やさしい先生)
AI-powered Japanese learning assistant for IBM Bob Hackathon (48-hour delivery target).

## Critical Non-Obvious Rules

### AI Model Configuration (CRITICAL)
- **Primary model**: `ibm/granite-4-h-small` (optimized for speed)
- **Fallback model**: `meta-llama/llama-3-3-70b-instruct`
- **BANNED model**: `mistral-medium-2505` - NEVER use this model for this hackathon
- **Endpoint**: `https://us-south.ml.cloud.ibm.com`
- Model constants MUST be defined in `config/prompts.py`

### Architecture Constraints
- **No database** - use in-memory caching only (not needed for hardcoded articles)
- **No authentication** - open access for demo
- **Monolithic Flask app** - single `app.py` for MVP, not microservices
- **Telegram bot is CORE MVP** - not optional, shares same Flask backend as web app
- Both web and Telegram interfaces must be demo-ready

### Prompt Engineering
- All prompts MUST request JSON-only responses (no additional text)
- Use combined analysis prompt to reduce API calls
- Prompts centralized in `config/prompts.py`
- Model parameters: `max_new_tokens=2000, temperature=0.3, top_p=0.9`

### Sample Articles (Hardcoded)
- NHK Web Easy requires authentication - cannot access programmatically
- Use hardcoded sample articles in `services/articles_service.py`
- 5 curated articles covering N5 to N2 difficulty levels
- Displayed as "Today's Articles" in UI and Telegram bot

### File Organization (Non-Standard)
- `services/` - watsonx.ai, sample articles, Telegram bot logic
- `config/prompts.py` - ALL AI prompts (not in services/)
- `utils/cache.py` - Simple TTL cache (not Redis/external)
- Telegram integration in `services/telegram_service.py` (CORE, not stretch)

### Development Priorities
1. watsonx.ai integration (granite-4-h-small)
2. Text analysis endpoint
3. Sample articles service (hardcoded)
4. Basic web UI
5. **Telegram bot (CORE MVP - Hours 16-20)**
6. Results display

### Demo Requirements
- Must show BOTH web interface AND Telegram bot
- Telegram bot demo video required
- Fast performance target: <5 seconds per analysis
- Sample content prepared for N5, N3, and casual Japanese

### Acceptable Hackathon Shortcuts
- Hardcoded prompts and sample articles in Python files (no database)
- No external API calls for content (articles are hardcoded)
- Minimal error handling
- No unit tests required
- Basic CSS (no pixel-perfect design)

### Features to AVOID
- User authentication
- Database persistence
- Progress tracking
- Microservices architecture
- Advanced NLP (let watsonx.ai handle it)