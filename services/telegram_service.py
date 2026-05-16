"""
Yasashii Sensei - Telegram Bot Service
CORE MVP feature - Telegram bot integration using polling mode.
Follows yasashii-telegram skill for message formatting and inline keyboards.
"""

import random
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from services.watsonx_service import WatsonxService
from services.articles_service import get_articles, get_article_by_id


class TelegramService:
    """Service for handling Telegram bot interactions."""
    
    def __init__(self, watsonx_service: WatsonxService):
        """
        Initialize Telegram bot service.
        
        Args:
            watsonx_service: Initialized WatsonxService instance
        """
        self.watsonx_service = watsonx_service
    
    # Inline Keyboard Helpers
    def get_welcome_keyboard(self):
        """Get welcome screen inline keyboard."""
        keyboard = [
            [
                InlineKeyboardButton("📰 Browse Articles", callback_data="articles"),
                InlineKeyboardButton("🎲 Random Article", callback_data="random")
            ],
            [
                InlineKeyboardButton("❓ How to Use", callback_data="help")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_articles_keyboard(self):
        """Get article selection inline keyboard."""
        keyboard = [
            [
                InlineKeyboardButton("1️⃣", callback_data="article_001"),
                InlineKeyboardButton("2️⃣", callback_data="article_002"),
                InlineKeyboardButton("3️⃣", callback_data="article_003")
            ],
            [
                InlineKeyboardButton("4️⃣", callback_data="article_004"),
                InlineKeyboardButton("5️⃣", callback_data="article_005")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_lesson_keyboard(self):
        """Get post-lesson navigation inline keyboard."""
        keyboard = [
            [
                InlineKeyboardButton("📰 More Articles", callback_data="articles"),
                InlineKeyboardButton("🎲 Random Article", callback_data="random")
            ],
            [
                InlineKeyboardButton("🏠 Home", callback_data="start")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_help_keyboard(self):
        """Get help screen inline keyboard."""
        keyboard = [
            [
                InlineKeyboardButton("📰 Browse Articles", callback_data="articles"),
                InlineKeyboardButton("🏠 Home", callback_data="start")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_error_keyboard(self):
        """Get error screen inline keyboard."""
        keyboard = [
            [
                InlineKeyboardButton("🔄 Try Again", callback_data="retry"),
                InlineKeyboardButton("🏠 Home", callback_data="start")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_not_japanese_keyboard(self):
        """Get not-Japanese-text inline keyboard."""
        keyboard = [
            [
                InlineKeyboardButton("📰 Browse Articles", callback_data="articles"),
                InlineKeyboardButton("🏠 Home", callback_data="start")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_article_preview_keyboard(self, article_id: str):
        """Get article preview keyboard with analyze button."""
        keyboard = [
            [
                InlineKeyboardButton("📖 Analyze This Article", callback_data=f"analyze_{article_id}"),
                InlineKeyboardButton("📰 Other Articles", callback_data="articles")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    # Command Handlers
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """🎌 *Welcome to やさしい先生!*
_Your Gentle Japanese Teacher_

I help you understand Japanese text by providing:
📚 Vocabulary with readings
📖 Grammar explanations
🌐 English translation
🏯 Cultural notes
📊 JLPT difficulty level

*How to use:*
Just send me any Japanese text and I will analyze it!"""
        
        if update.message:
            await update.message.reply_text(
                welcome_message,
                parse_mode='Markdown',
                reply_markup=self.get_welcome_keyboard()
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = """❓ *やさしい先生 Commands*

💬 *[Japanese text]* — Analyze any Japanese text
📰 /articles — Browse today's sample articles
🔄 /start — Show welcome message
❓ /help — Show this help message

*Tips:*
• Works with any Japanese text
• Paste from manga, news, emails, signs
• Any JLPT level from N5 to N1"""
        
        if update.message:
            await update.message.reply_text(
                help_message,
                parse_mode='Markdown',
                reply_markup=self.get_help_keyboard()
            )
    
    async def articles_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /articles command."""
        articles = get_articles()
        
        message = """📰 *Today's Articles*
Choose an article to analyze:

"""
        
        for i, article in enumerate(articles, 1):
            emoji_num = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"][i-1]
            message += f"{emoji_num} {article['title']} [{article['difficulty']} · {article['topic']}]\n"
        
        if update.message:
            await update.message.reply_text(
                message,
                parse_mode='Markdown',
                reply_markup=self.get_articles_keyboard()
            )
    
    # Callback Query Handler
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button callbacks."""
        query = update.callback_query
        if not query:
            return
            
        await query.answer()
        
        callback_data = query.data
        if not callback_data:
            return
        
        if callback_data == "start":
            # Show welcome message
            welcome_message = """🎌 *Welcome to やさしい先生!*
_Your Gentle Japanese Teacher_

I help you understand Japanese text by providing:
📚 Vocabulary with readings
📖 Grammar explanations
🌐 English translation
🏯 Cultural notes
📊 JLPT difficulty level

*How to use:*
Just send me any Japanese text and I will analyze it!"""
            
            await query.edit_message_text(
                welcome_message,
                parse_mode='Markdown',
                reply_markup=self.get_welcome_keyboard()
            )
        
        elif callback_data == "articles":
            # Show article list
            articles = get_articles()
            
            message = """📰 *Today's Articles*
Choose an article to analyze:

"""
            
            for i, article in enumerate(articles, 1):
                emoji_num = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"][i-1]
                message += f"{emoji_num} {article['title']} [{article['difficulty']} · {article['topic']}]\n"
            
            await query.edit_message_text(
                message,
                parse_mode='Markdown',
                reply_markup=self.get_articles_keyboard()
            )
        
        elif callback_data == "random":
            # Pick random article and show preview
            articles = get_articles()
            article = random.choice(articles)
            
            if query.message:
                # Show article preview
                preview_message = f"📰 *{article['title']}*\n"
                preview_message += f"[{article['difficulty']} · {article['topic']}]\n\n"
                preview_message += f"{article['content']}\n\n"
                preview_message += "─────────────────"
                
                await query.message.reply_text(
                    preview_message,
                    parse_mode='Markdown',
                    reply_markup=self.get_article_preview_keyboard(article['id'])
                )
        
        elif callback_data == "help":
            # Show help message
            help_message = """❓ *やさしい先生 Commands*

💬 *[Japanese text]* — Analyze any Japanese text
📰 /articles — Browse today's sample articles
🔄 /start — Show welcome message
❓ /help — Show this help message

*Tips:*
• Works with any Japanese text
• Paste from manga, news, emails, signs
• Any JLPT level from N5 to N1"""
            
            await query.edit_message_text(
                help_message,
                parse_mode='Markdown',
                reply_markup=self.get_help_keyboard()
            )
        
        elif callback_data.startswith("article_"):
            # Show article preview (not analyze yet)
            article_id = callback_data
            article = get_article_by_id(article_id)
            
            if not article:
                if query.message:
                    await query.message.reply_text("❌ Article not found.")
                return
            
            if query.message:
                # Show article preview
                preview_message = f"📰 *{article['title']}*\n"
                preview_message += f"[{article['difficulty']} · {article['topic']}]\n\n"
                preview_message += f"{article['content']}\n\n"
                preview_message += "─────────────────"
                
                await query.message.reply_text(
                    preview_message,
                    parse_mode='Markdown',
                    reply_markup=self.get_article_preview_keyboard(article['id'])
                )
        
        elif callback_data.startswith("analyze_"):
            # Analyze the article (user tapped "Analyze This Article")
            article_id = callback_data.replace("analyze_", "")
            article = get_article_by_id(article_id)
            
            if not article:
                if query.message:
                    await query.message.reply_text("❌ Article not found.")
                return
            
            if query.message:
                # Send loading message
                loading_msg = await query.message.reply_text(
                    "🔍 *Analyzing Japanese text...*\nThis may take a few seconds ⏳",
                    parse_mode='Markdown'
                )
                
                # Send typing action
                await context.bot.send_chat_action(chat_id=query.message.chat_id, action="typing")
                
                try:
                    # Analyze article using watsonx.ai
                    print(f"Analyzing article: {article_id}")
                    print(f"Article content: {article['content'][:100]}...")
                    
                    analysis = self.watsonx_service.analyze_text(article['content'])
                    
                    # Debug output
                    print(f"Analysis result keys: {list(analysis.keys())}")
                    print(f"Vocab count: {len(analysis.get('vocabulary', []))}")
                    print(f"Grammar count: {len(analysis.get('grammar_points', []))}")
                    
                    # Format response for Telegram
                    response = self.format_analysis_for_telegram(analysis, article['content'])
                    
                    # Delete loading message
                    await loading_msg.delete()
                    
                    # Send response (split if too long)
                    if len(response) > 4096:
                        # Split into chunks at section boundaries
                        chunks = self.split_message(response)
                        for chunk in chunks:
                            await query.message.reply_text(chunk, parse_mode='Markdown')
                        # Send navigation buttons after last chunk
                        await query.message.reply_text(
                            "─────────────────",
                            parse_mode='Markdown',
                            reply_markup=self.get_lesson_keyboard()
                        )
                    else:
                        await query.message.reply_text(
                            response,
                            parse_mode='Markdown',
                            reply_markup=self.get_lesson_keyboard()
                        )
                
                except Exception as e:
                    # Delete loading message
                    await loading_msg.delete()
                    
                    print(f"Analysis error: {str(e)}")
                    
                    # Send error message
                    error_message = """⚠️ *Analysis Error*

Sorry, I couldn't analyze that text right now.
Please try again in a moment."""
                    
                    await query.message.reply_text(
                        error_message,
                        parse_mode='Markdown',
                        reply_markup=self.get_error_keyboard()
                    )
        
        elif callback_data == "retry":
            # Ask user to resend text
            if query.message:
                await query.message.reply_text(
                    "Please send me Japanese text to analyze.",
                    parse_mode='Markdown'
                )
    
    # Message Handler
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages - analyze Japanese text."""
        if not update.message or not update.message.text:
            return
            
        text = update.message.text
        
        # Check if text contains Japanese characters
        if not self.contains_japanese(text):
            not_japanese_message = """🤔 *That doesn't look like Japanese text*

Please send Japanese text for analysis.

*Examples of valid input:*
• Paste text from a Japanese website
• Copy from a Japanese app or game
• Type hiragana, katakana, or kanji"""
            
            await update.message.reply_text(
                not_japanese_message,
                parse_mode='Markdown',
                reply_markup=self.get_not_japanese_keyboard()
            )
            return
        
        # Validate text length
        if len(text) > 5000:
            await update.message.reply_text(
                "❌ Text is too long. Please send text under 5000 characters.",
                parse_mode='Markdown'
            )
            return
        
        # Send loading message with typing action
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        
        loading_msg = await update.message.reply_text(
            "🔍 *Analyzing Japanese text...*\nThis may take a few seconds ⏳",
            parse_mode='Markdown'
        )
        
        # Analyze and send result
        try:
            await self.analyze_and_send(update.message, text)
            # Delete loading message
            await loading_msg.delete()
        except Exception as e:
            # Delete loading message
            await loading_msg.delete()
            
            # Send error message
            error_message = """⚠️ *Analysis Error*

Sorry, I couldn't analyze that text right now.
Please try again in a moment."""
            
            await update.message.reply_text(
                error_message,
                parse_mode='Markdown',
                reply_markup=self.get_error_keyboard()
            )
    
    async def analyze_and_send(self, message, text: str):
        """Analyze text and send formatted result."""
        try:
            # Analyze text using watsonx.ai
            analysis = self.watsonx_service.analyze_text(text)
            
            # Format response for Telegram
            response = self.format_analysis_for_telegram(analysis, text)
            
            # Send response (split if too long)
            if len(response) > 4096:
                # Split into chunks at section boundaries
                chunks = self.split_message(response)
                for chunk in chunks:
                    await message.reply_text(chunk, parse_mode='Markdown')
                # Send navigation buttons after last chunk
                await message.reply_text(
                    "─────────────────",
                    parse_mode='Markdown',
                    reply_markup=self.get_lesson_keyboard()
                )
            else:
                await message.reply_text(
                    response,
                    parse_mode='Markdown',
                    reply_markup=self.get_lesson_keyboard()
                )
        
        except Exception as e:
            raise e
    
    def format_analysis_for_telegram(self, analysis: dict, original_text: str) -> str:
        """Format analysis results following yasashii-telegram skill."""
        # Header
        message = "🎌 *やさしい先生 Analysis*\n"
        message += f"📊 JLPT Level: *{analysis.get('jlpt_level', 'N3')}*\n\n"
        
        # Vocabulary section
        vocab = analysis.get('vocabulary', [])
        if vocab:
            message += "📚 *Vocabulary*\n\n"
            for v in vocab[:10]:  # Show up to 10 vocab items
                word = v.get('word', '')
                reading = v.get('reading', '')
                meaning = v.get('meaning', '')
                jlpt = v.get('jlpt_level', '')
                pos = v.get('part_of_speech', 'noun')
                
                if jlpt:
                    message += f"• {word} ({reading}) — {meaning} [{pos}, {jlpt}]\n"
                else:
                    message += f"• {word} ({reading}) — {meaning} [{pos}]\n"
            message += "\n"
        
        # Grammar section (only if present)
        grammar = analysis.get('grammar_points', [])
        if grammar:
            message += "📖 *Grammar Patterns*\n\n"
            for g in grammar[:5]:  # Show up to 5 grammar points
                pattern = g.get('pattern', '')
                explanation = g.get('explanation', '')
                example = g.get('example', '')
                
                message += f"• *{pattern}* — {explanation}\n"
                if example:
                    message += f"  Example: {example}\n"
            message += "\n"
        
        # Translation section
        translation = analysis.get('translation', 'N/A')
        message += "🌐 *Translation*\n"
        message += f"{translation}\n\n"
        
        # Cultural notes section (only if present)
        cultural = analysis.get('cultural_notes', [])
        if cultural:
            message += "🏯 *Cultural Notes*\n\n"
            for note in cultural[:2]:  # Show up to 2 cultural notes
                topic = note.get('topic', '')
                explanation = note.get('explanation', '')
                message += f"*{topic}:* {explanation}\n\n"
        
        # Footer separator
        message += "─────────────────"
        
        return message
    
    def split_message(self, message: str, max_length: int = 4096) -> list:
        """Split long message into chunks at section boundaries."""
        if len(message) <= max_length:
            return [message]
        
        chunks = []
        current_chunk = ""
        
        # Split by sections (double newline)
        sections = message.split("\n\n")
        
        for section in sections:
            if len(current_chunk) + len(section) + 2 <= max_length:
                current_chunk += section + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = section + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def contains_japanese(self, text: str) -> bool:
        """Check if text contains Japanese characters."""
        for char in text:
            # Hiragana: 3040-309F
            # Katakana: 30A0-30FF
            # Kanji: 4E00-9FFF
            code = ord(char)
            if (0x3040 <= code <= 0x309F or  # Hiragana
                0x30A0 <= code <= 0x30FF or  # Katakana
                0x4E00 <= code <= 0x9FFF):   # Kanji
                return True
        return False


def create_telegram_bot(bot_token: str, watsonx_service: WatsonxService):
    """
    Create and run Telegram bot with proper initialization.
    
    Args:
        bot_token: Telegram bot token from BotFather
        watsonx_service: Initialized WatsonxService instance
    """
    # Create service instance
    service = TelegramService(watsonx_service)
    
    # Build application
    application = Application.builder().token(bot_token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", service.start_command))
    application.add_handler(CommandHandler("help", service.help_command))
    application.add_handler(CommandHandler("articles", service.articles_command))
    
    # Callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(service.handle_callback))
    
    # Text message handler
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, service.handle_message)
    )
    
    # Run polling (this handles the event loop internally)
    print("🤖 Telegram bot started (polling mode)...")
    application.run_polling(allowed_updates=["message", "callback_query"])

# Made with Bob
