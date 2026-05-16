"""
Yasashii Sensei - Main Flask Application
AI-powered Japanese learning assistant with web and Telegram interfaces.
"""

import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from services.watsonx_service import WatsonxService
from services.articles_service import (
    get_articles,
    get_article_by_id,
    get_articles_by_difficulty,
    get_articles_by_topic
)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Enable CORS for frontend
CORS(app)

# Initialize services
watsonx_service = None

def get_watsonx_service():
    """Lazy initialization of WatsonxService."""
    global watsonx_service
    if watsonx_service is None:
        watsonx_service = WatsonxService()
    return watsonx_service


# ============================================================================
# Web Routes
# ============================================================================

@app.route('/')
def index():
    """Serve the homepage."""
    return render_template('index.html')


@app.route('/results')
def results():
    """Serve the results page."""
    return render_template('results.html')


# ============================================================================
# API Routes
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON with service status
    """
    try:
        service = get_watsonx_service()
        model_info = service.get_model_info()
        
        return jsonify({
            'status': 'healthy',
            'service': 'Yasashii Sensei',
            'watsonx': {
                'connected': True,
                'current_model': model_info['current_model'],
                'using_fallback': model_info['using_fallback']
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'service': 'Yasashii Sensei',
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Analyze Japanese text using watsonx.ai.
    
    Request JSON:
        {
            "text": "Japanese text to analyze",
            "source": "paste|article"  # optional
        }
    
    Returns:
        JSON with comprehensive analysis including:
        - jlpt_level
        - vocabulary
        - grammar_points
        - translation
        - cultural_notes
        - comprehension_questions
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON',
                'message': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'text' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Field "text" is required'
            }), 400
        
        japanese_text = data['text'].strip()
        
        # Validate text is not empty
        if not japanese_text:
            return jsonify({
                'error': 'Empty text',
                'message': 'Text cannot be empty'
            }), 400
        
        # Validate text length
        max_length = int(os.getenv('MAX_TEXT_LENGTH', 5000))
        if len(japanese_text) > max_length:
            return jsonify({
                'error': 'Text too long',
                'message': f'Text must be less than {max_length} characters'
            }), 400
        
        # Get source (optional)
        source = data.get('source', 'paste')
        
        # Analyze text with watsonx.ai
        service = get_watsonx_service()
        analysis = service.analyze_text(japanese_text)
        
        # Add source to response
        analysis['source'] = source
        analysis['original_text'] = japanese_text
        
        return jsonify(analysis), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500


@app.route('/api/articles', methods=['GET'])
def get_all_articles():
    """
    Get all sample articles.
    
    Query parameters:
        difficulty: Filter by JLPT level (N5, N4, N3, N2, N1)
        topic: Filter by topic (culture, news, lifestyle, technology, nature)
    
    Returns:
        JSON array of articles
    """
    try:
        # Get query parameters
        difficulty = request.args.get('difficulty')
        topic = request.args.get('topic')
        
        # Filter articles
        if difficulty:
            articles = get_articles_by_difficulty(difficulty.upper())
        elif topic:
            articles = get_articles_by_topic(topic.lower())
        else:
            articles = get_articles()
        
        return jsonify({
            'articles': articles,
            'count': len(articles)
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error fetching articles: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch articles',
            'message': str(e)
        }), 500


@app.route('/api/articles/<article_id>', methods=['GET'])
def get_article(article_id):
    """
    Get a specific article by ID.
    
    Args:
        article_id: Article ID (e.g., "article_001")
    
    Returns:
        JSON with article data or 404 if not found
    """
    try:
        article = get_article_by_id(article_id)
        
        if article is None:
            return jsonify({
                'error': 'Article not found',
                'message': f'No article found with ID: {article_id}'
            }), 404
        
        return jsonify(article), 200
        
    except Exception as e:
        app.logger.error(f"Error fetching article {article_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch article',
            'message': str(e)
        }), 500


@app.route('/api/telegram/webhook', methods=['POST'])
def telegram_webhook():
    """
    Telegram bot webhook endpoint.
    
    Receives updates from Telegram and processes them.
    This is a placeholder - full implementation in services/telegram_service.py
    
    Returns:
        JSON response for Telegram
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        update = request.get_json()
        
        # Log webhook received
        app.logger.info(f"Telegram webhook received: {update.get('update_id', 'unknown')}")
        
        # TODO: Process update with TelegramService
        # For now, return success
        return jsonify({'ok': True}), 200
        
    except Exception as e:
        app.logger.error(f"Telegram webhook error: {str(e)}")
        return jsonify({
            'error': 'Webhook processing failed',
            'message': str(e)
        }), 500


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    app.logger.error(f"Internal error: {str(error)}")
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    return render_template('index.html'), 500


@app.errorhandler(413)
def request_too_large(error):
    """Handle request too large errors."""
    return jsonify({
        'error': 'Request too large',
        'message': 'The request payload is too large'
    }), 413


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == '__main__':
    # Get configuration from environment
    flask_env = os.getenv('FLASK_ENV', 'development')
    flask_debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    flask_port = int(os.getenv('FLASK_PORT', 5000))
    flask_host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    # Print startup information
    print("=" * 60)
    print("🎓 Yasashii Sensei (やさしい先生)")
    print("AI-Powered Japanese Learning Assistant")
    print("=" * 60)
    print(f"Environment: {flask_env}")
    print(f"Debug Mode: {flask_debug}")
    print(f"Server: http://{flask_host}:{flask_port}")
    print("=" * 60)
    print("\nAvailable Routes:")
    print("  GET  /                    → Homepage")
    print("  GET  /results             → Results page")
    print("  POST /api/analyze         → Analyze Japanese text")
    print("  GET  /api/articles        → Get all articles")
    print("  GET  /api/articles/<id>   → Get article by ID")
    print("  GET  /api/health          → Health check")
    print("  POST /api/telegram/webhook → Telegram webhook")
    print("=" * 60)
    
    # Run Flask app
    app.run(
        host=flask_host,
        port=flask_port,
        debug=flask_debug
    )

# Made with Bob