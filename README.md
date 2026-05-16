# やさしい先生 (Yasashii Sensei)

**AI-Powered Japanese Learning Assistant**  
IBM Bob Hackathon Project - 48-Hour Delivery Target

## Quick Start

Core services are working. watsonx.ai integration, 
articles service, and web frontend complete.
Telegram bot in progress.

## Project Overview

Yasashii Sensei helps Japanese learners understand authentic content using IBM watsonx.ai. Users can paste Japanese text or browse NHK Web Easy articles to receive:
- Context-aware vocabulary explanations
- Grammar breakdowns
- English translations
- JLPT difficulty estimation
- Cultural notes

**Two interfaces**: Web app + Telegram bot (both share the same Flask backend)

## Critical Configuration

### AI Models (IMPORTANT)
- **Primary**: `meta-llama/llama-4-maverick-17b-128e-instruct-fp8`
- **Fallback**: `meta-llama/llama-3-3-70b-instruct`
- **BANNED**: `mistral-medium-2505` (do not use for this hackathon)

### Architecture Constraints
- No database (in-memory caching only)
- No authentication (open demo access)
- Monolithic Flask app (single `app.py`)
- Telegram bot is CORE MVP (not optional)

## Documentation

- [`YASASHII_SENSEI_BOB_BRIEF.md`](YASASHII_SENSEI_BOB_BRIEF.md) - Complete technical specification
- [`AGENTS.md`](AGENTS.md) - AI assistant guidance (general)
- `.bob-rules-code-AGENTS.md` - Code mode specific rules
- `.bob-rules-advanced-AGENTS.md` - Advanced mode specific rules
- `.bob-rules-ask-AGENTS.md` - Ask mode specific rules
- `.bob-rules-plan-AGENTS.md` - Plan mode specific rules

## Current Status
- ✅ watsonx.ai integration (Maverick model)
- ✅ Articles service (5 sample articles)
- ✅ Web frontend working
- ✅ Vocabulary, grammar, cultural notes displaying
- 🔄 Telegram bot in progress
- 🔲 Demo video
- 🔲 Submission

## Setup
1. Clone repo
2. Create venv: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill credentials
6. Run: `python3 app.py`
## Development Phases

**Phase 1 (Hours 0-8)**: Foundation
- Project setup
- watsonx.ai integration
- Basic web UI

**Phase 2 (Hours 8-20)**: Core Features
- Results display
- NHK article browser
- **Telegram bot integration (CORE MVP)**
- Polish and refinement

**Phase 3 (Hours 20-32)**: Enhancement
- Cultural notes (stretch)
- Comprehension questions (stretch)
- Testing and bug fixes

**Phase 4 (Hours 32-48)**: Demo Preparation
- Demo content preparation
- Telegram bot demo video
- Final polish
- Presentation materials

## Tech Stack

- **Backend**: Python Flask
- **AI**: IBM watsonx.ai (meta-llama/llama-4-maverick-17b-128e-instruct-fp8)
- **Frontend**: HTML/CSS/JavaScript
- **Messaging**: Telegram Bot API
- **Content**:  Hardcoded sample articles (NHK requires auth)

## License

Hackathon project - IBM Bob Hackathon 2026