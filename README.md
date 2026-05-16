# やさしい先生 (Yasashii Sensei)

**AI-Powered Japanese Learning Assistant**  
IBM Bob Hackathon Project - 48-Hour Delivery Target

## 🎯 Project Overview

Yasashii Sensei is a complete Japanese learning assistant that helps learners understand authentic Japanese content using IBM watsonx.ai. The system provides intelligent analysis of Japanese text through both a web interface and a Telegram bot.

### What We've Built

**Two Complete Interfaces:**
1. **Web Application** - Flask-based web UI for desktop/mobile browsers
2. **Telegram Bot** - Full-featured bot with inline keyboards and interactive lessons

**Core Features:**
- 📊 JLPT difficulty level assessment (N5-N1)
- 📚 Vocabulary breakdown with readings and meanings
- 📖 Grammar pattern explanations with examples
- 🌐 English translations
- 🏯 Cultural notes and context
- 🔊 Text-to-Speech audio pronunciation (IBM Watson TTS)
- 🎲 5 curated sample articles (N5-N2 difficulty)
- 🤖 Interactive Telegram bot with button navigation

## 🚀 Quick Start

### Web Application
```bash
# 1. Setup environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure .env file
cp .env.example .env
# Edit .env and add your credentials:
# - WATSONX_API_KEY
# - WATSONX_PROJECT_ID
# - IBM_TTS_API_KEY (CORE feature)
# - IBM_TTS_URL (CORE feature)
# - TELEGRAM_BOT_TOKEN (optional for web-only)

# 3. Run web app
python app.py
# Visit http://localhost:5001
```

### Telegram Bot
```bash
# 1. Complete web app setup above
# 2. Get bot token from @BotFather on Telegram
# 3. Add TELEGRAM_BOT_TOKEN to .env
# 4. Run bot
python bot.py
```

## 🎌 How to Use

### Web Interface
1. Visit http://localhost:5001
2. Paste any Japanese text or select a sample article
3. Click "Analyze" to get instant breakdown
4. View vocabulary, grammar, translation, and cultural notes

### Telegram Bot
1. Start chat with your bot on Telegram
2. Send `/start` to see welcome message
3. Choose from:
   - **Browse Articles** - Select from 5 curated articles
   - **Random Article** - Get a surprise article
   - **Send Japanese text** - Analyze any text directly

**Article Flow:**
1. Select article → Read Japanese text first
2. Tap "📖 Analyze This Article" → Get full lesson
3. Navigate with inline buttons

## 🏗️ Architecture

### Tech Stack
- **Backend**: Python 3.11+ with Flask
- **AI Engine**: IBM watsonx.ai
  - Primary: `meta-llama/llama-4-maverick-17b-128e-instruct-fp8`
  - Fallback: `meta-llama/llama-3-3-70b-instruct`
- **TTS**: IBM Watson Text-to-Speech (CORE feature)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Bot Framework**: python-telegram-bot v20+
- **Content**: 5 hardcoded sample articles (N5-N2)

### Project Structure
```
yasashii-sensei/
├── app.py                      # Flask web application
├── bot.py                      # Telegram bot entry point
├── config/
│   └── prompts.py             # AI prompts and model config
├── services/
│   ├── watsonx_service.py     # watsonx.ai integration
│   ├── articles_service.py    # Sample articles
│   ├── tts_service.py         # Text-to-Speech integration
│   └── telegram_service.py    # Telegram bot logic
├── templates/                  # HTML templates
├── static/                     # CSS, JS, assets
└── utils/                      # Helper utilities
```

## 🤖 Telegram Bot Features

### Interactive Commands
- `/start` - Welcome message with navigation buttons
- `/help` - Command reference and tips
- `/articles` - Browse today's articles

### Inline Keyboard Navigation
- **Welcome Screen**: Browse Articles, Random Article, How to Use
- **Article List**: Number buttons (1️⃣-5️⃣) for selection
- **Article Preview**: Analyze This Article, Other Articles
- **Post-Lesson**: More Articles, Random Article, Home
- **Error Handling**: Try Again, Home

### Smart Features
- ✅ Japanese text detection (hiragana, katakana, kanji)
- ✅ Loading indicators with typing animation
- ✅ Message splitting for long content (4096 char limit)
- ✅ Error recovery with retry buttons
- ✅ Article preview before analysis (read Japanese first!)

## 📊 Sample Articles

5 curated articles covering different JLPT levels:

1. **今日の天気** (N5 · lifestyle) - Simple weather description
2. **東京で新しい美術館がオープン** (N4 · culture) - Museum opening
3. **新しいスマートフォンアプリが人気** (N3 · technology) - App popularity
4. **環境保護のための新しい政策が発表される** (N2 · news) - Environmental policy
5. **週末のカフェ巡り** (N3 · lifestyle) - Casual cafe visit

## ⚙️ Configuration

### Critical Settings

**AI Models** (defined in `config/prompts.py`):
- Primary: `meta-llama/llama-4-maverick-17b-128e-instruct-fp8` '(fast, optimized)
- Fallback: `meta-llama/llama-3-3-70b-instruct`
- **BANNED**: `mistral-medium-2505` (not for this hackathon)

**Model Parameters**:
- `max_new_tokens`: 1500
- `temperature`: 0.1
- `top_p`: 0.9

**Architecture Constraints**:
- ❌ No database (in-memory caching only)
- ❌ No authentication (open demo access)
- ✅ Monolithic Flask app (single `app.py`)
- ✅ Telegram bot is CORE MVP (not optional)

### Environment Variables

Required in `.env`:
```bash
# IBM watsonx.ai
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# IBM Watson Text-to-Speech (CORE feature)
IBM_TTS_API_KEY=your_tts_api_key_here
IBM_TTS_URL=https://api.us-south.text-to-speech.watson.cloud.ibm.com
IBM_TTS_VOICE=ja-JP_EmiV3Voice

# Flask
FLASK_PORT=5001
FLASK_DEBUG=True
SECRET_KEY=change_this_to_random_string

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
```

## 🎯 Current Status

### ✅ Completed Features
- [x] watsonx.ai integration with llama-4-maverick
- [x] Combined analysis prompt (single API call)
- [x] 5 sample articles (N5-N2 difficulty)
- [x] Web frontend with analysis display
- [x] Vocabulary with readings and JLPT levels
- [x] Grammar patterns with examples
- [x] English translations
- [x] Cultural notes
- [x] **IBM Watson Text-to-Speech integration (CORE)**
- [x] **Complete Telegram bot with inline keyboards**
- [x] Article preview flow (read before analysis)
- [x] Error handling and recovery
- [x] Japanese text detection
- [x] Message formatting per yasashii-telegram skill
- [x] Text-to-Speech (IBM Watson TTS)

### 🔄 In Progress
- [ ] Demo video recording
- [ ] Final testing and polish

## 🐛 Troubleshooting

### Web App Issues
```bash
# Check if Flask is running
curl http://localhost:5001

# View logs
python app.py  # Check console output

# Test watsonx.ai connection
python -c "from services.watsonx_service import WatsonxService; print('OK')"
```

### Telegram Bot Issues
```bash
# Verify bot token
# Check .env has TELEGRAM_BOT_TOKEN set

# Test bot startup
python bot.py
# Should see: "🤖 Telegram bot started (polling mode)..."

# Check for errors in console output
# Debug prints show analysis flow
```

### Common Issues
1. **Empty analysis results**: Check debug output for API errors
2. **Bot not responding**: Verify token with @BotFather
3. **Import errors**: Ensure all dependencies installed: `pip install -r requirements.txt`
4. **Event loop errors**: Fixed - using correct python-telegram-bot v20+ pattern

## 📚 Documentation

- [`YASASHII_SENSEI_BOB_BRIEF.md`](YASASHII_SENSEI_BOB_BRIEF.md) - Complete technical specification
- [`AGENTS.md`](AGENTS.md) - AI assistant guidance
- [`.bob/skills/yasashii-frontend/SKILL.md`](.bob/skills/yasashii-frontend/SKILL.md) - Frontend skill
- [`.bob/skills/yasashii-telegram/SKILL.md`](.bob/skills/yasashii-telegram/SKILL.md) - Telegram formatting skill

## 🎓 Learning Resources

The system is designed to help with:
- Reading Japanese news articles
- Understanding manga and anime dialogue
- Analyzing Japanese emails and messages
- Learning from authentic Japanese content
- Preparing for JLPT exams

## 🤝 Contributing

This is a hackathon project built for IBM Bob Hackathon 2026. The codebase prioritizes:
- Fast delivery (48-hour target)
- Working features over perfect code
- Hardcoded content over complex data pipelines
- Demo-ready functionality

## 📝 License

Hackathon project - IBM Bob Hackathon 2026

## 🙏 Acknowledgments

- IBM Bob IDE for AI-assisted development throughout the SDLC
- IBM watsonx.ai for powerful language models
- Telegram Bot API for messaging platform
- NHK Web Easy for inspiration (articles are hardcoded samples)
- Japanese language learning community

---

**Built with ❤️ for Japanese learners**  
やさしい先生 - Your Gentle Japanese Teacher