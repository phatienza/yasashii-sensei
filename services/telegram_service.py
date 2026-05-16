"""
Yasashii Sensei - Telegram Bot Service
CORE MVP feature - Telegram bot integration using polling mode.
"""

from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from services.watsonx_service import WatsonxService
from services.articles_service import get_articles, get_article_by_id


class TelegramService:
    """Service for handling Telegram bot interactions."""
    
    def __init__(self, bot_token: str, watsonx_service: WatsonxService):
        """
        Initialize Telegram bot service.
        
        Args:
            bot_token: Telegram bot token from BotFather
            watsonx_service: Initialized WatsonxService instance
        """
        self.bot_token = bot_token
        self.watsonx_service = watsonx_service
        self.application = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command.
        
        Args:
            update: Telegram update object
            context: Callback context
        """
        welcome_message = """
🌸 *やさしい先生 (Yasashii Sensei)* へようこそ！

I'm your AI Japanese learning assistant! I can help you:

📝 *Analyze Japanese text*
Just send me any Japanese text and I'll provide:
• JLPT level assessment
• Vocabulary breakdown with readings
• Grammar explanations
• English translation
• Cultural notes
• Comprehension questions

📰 *Browse sample articles*
Use /articles to see today's curated Japanese articles

❓ *Get help*
Use /help to see all available commands

*How to use:*
Simply send me Japanese text and I'll analyze it for you!

例: 今日は天気がいいです。
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /help command.
        
        Args:
            update: Telegram update object
            context: Callback context
        """
        help_message = """
📚 *Available Commands:*

/start - Welcome message and introduction
/help - Show this help message
/articles - Browse today's sample articles

*How to analyze text:*
Just send me any Japanese text directly (no command needed)!

*Examples:*
• 今日は天気がいいです。
• 東京で新しい美術館がオープンしました。
• 日本語を勉強しています。

I'll analyze the text and provide:
✓ JLPT level
✓ Vocabulary with readings
✓ Grammar explanations
✓ English translation
✓ Cultural notes
✓ Comprehension questions

*Tips:*
• Send text between 10-5000 characters
• Text must contain Japanese characters
• Analysis takes 3-5 seconds
        """
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def articles_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /articles command - show today's sample articles.
        
        Args:
            update: Telegram update object
            context: Callback context
        """
        articles = get_articles()
        
        message = "📰 *Today's Articles (今日の記事)*\n\n"
        message += "Select an article to analyze:\n\n"
        
        for i, article in enumerate(articles, 1):
            difficulty_emoji = {
                "N5": "🟢",
                "N4": "🔵", 
                "N3": "🟡",
                "N2": "🟠",
                "N1": "🔴"
            }.get(article["difficulty"], "⚪")
            
            topic_emoji = {
                "lifestyle": "🏠",
                "culture": "🎨",
                "technology": "💻",
                "news": "📰",
                "nature": "🌿"
            }.get(article["topic"], "📄")
            
            message += f"{i}. {difficulty_emoji} *{article['title']}*\n"
            message += f"   {topic_emoji} {article['topic'].title()} | Level: {article['difficulty']}\n"
            message += f"   `/article_{article['id'].split('_')[1]}`\n\n"
        
        message += "\n💡 *Tip:* Click any command above to load the article!"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def article_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /article_XXX commands - load specific article.
        
        Args:
            update: Telegram update object
            context: Callback context
        """
        # Extract article number from command
        command_text = update.message.text
        article_num = command_text.split('_')[-1]
        article_id = f"article_{article_num}"
        
        article = get_article_by_id(article_id)
        
        if not article:
            await update.message.reply_text("❌ Article not found. Use /articles to see available articles.")
            return
        
        # Send article content
        article_message = f"📄 *{article['title']}*\n\n"
        article_message += f"📅 {article['date']} | 📊 {article['difficulty']} | 🏷️ {article['topic']}\n\n"
        article_message += f"{article['content']}\n\n"
        article_message += "🔄 Analyzing... please wait..."
        
        await update.message.reply_text(article_message, parse_mode='Markdown')
        
        # Analyze the article
        await self.handle_message(update, context, text_override=article['content'])
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text_override: Optional[str] = None):
        """
        Handle text messages - analyze Japanese text.
        
        Args:
            update: Telegram update object
            context: Callback context
            text_override: Optional text to analyze instead of message text
        """
        text = text_override or update.message.text
        
        # Validate text
        if not text or len(text.strip()) < 1:
            await update.message.reply_text("❌ Please send some Japanese text to analyze.")
            return
        
        if len(text) > 5000:
            await update.message.reply_text("❌ Text is too long. Please send text under 5000 characters.")
            return
        
        # Send processing message
        if not text_override:
            processing_msg = await update.message.reply_text("🔄 Analyzing your text... please wait...")
        
        try:
            # Analyze text using watsonx.ai
            analysis = self.watsonx_service.analyze_text(text)
            
            # Format response for Telegram
            response = self.format_analysis_for_telegram(analysis, text)
            
            # Send response (split if too long)
            if len(response) > 4096:
                # Split into chunks
                chunks = [response[i:i+4096] for i in range(0, len(response), 4096)]
                for chunk in chunks:
                    await update.message.reply_text(chunk, parse_mode='Markdown')
            else:
                await update.message.reply_text(response, parse_mode='Markdown')
            
            # Delete processing message
            if not text_override:
                await processing_msg.delete()
        
        except Exception as e:
            error_message = f"❌ *Analysis failed*\n\n"
            error_message += f"Error: {str(e)}\n\n"
            error_message += "Please try again or use /help for assistance."
            
            await update.message.reply_text(error_message, parse_mode='Markdown')
            
            if not text_override:
                await processing_msg.delete()
    
    def format_analysis_for_telegram(self, analysis: dict, original_text: str) -> str:
        """
        Format analysis results for Telegram markdown.
        
        Args:
            analysis: Analysis results from watsonx.ai
            original_text: Original Japanese text
            
        Returns:
            Formatted message string
        """
        message = "✅ *Analysis Complete*\n\n"
        
        # JLPT Level
        level_emoji = {
            "N5": "🟢",
            "N4": "🔵",
            "N3": "🟡",
            "N2": "🟠",
            "N1": "🔴"
        }.get(analysis.get("jlpt_level", "N3"), "⚪")
        
        message += f"📊 *JLPT Level:* {level_emoji} {analysis.get('jlpt_level', 'N3')}\n\n"
        
        # Original Text
        message += f"📝 *Original Text:*\n{original_text}\n\n"
        
        # Translation
        message += f"🌐 *Translation:*\n{analysis.get('translation', 'N/A')}\n\n"
        
        # Vocabulary (top 5)
        vocab = analysis.get('vocabulary', [])[:5]
        if vocab:
            message += "📚 *Key Vocabulary:*\n"
            for v in vocab:
                message += f"• {v.get('word', '')} ({v.get('reading', '')}) - {v.get('meaning', '')}\n"
            message += "\n"
        
        # Grammar Points (top 3)
        grammar = analysis.get('grammar_points', [])[:3]
        if grammar:
            message += "📖 *Grammar Points:*\n"
            for g in grammar:
                message += f"• {g.get('pattern', '')}: {g.get('explanation', '')}\n"
            message += "\n"
        
        # Cultural Notes
        cultural = analysis.get('cultural_notes', [])
        if cultural:
            message += "🎎 *Cultural Notes:*\n"
            for note in cultural[:2]:
                message += f"• {note.get('topic', '')}: {note.get('explanation', '')}\n"
            message += "\n"
        
        # Comprehension Questions
        questions = analysis.get('comprehension_questions', [])
        if questions:
            message += "❓ *Comprehension Questions:*\n"
            for i, q in enumerate(questions[:2], 1):
                message += f"{i}. {q.get('question', '')}\n"
            message += "\n"
        
        message += "💡 Send more Japanese text to analyze!"
        
        return message
    
    def setup_handlers(self):
        """Set up command and message handlers."""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("articles", self.articles_command))
        
        # Dynamic article handlers
        for i in range(1, 6):
            article_num = f"{i:03d}"
            self.application.add_handler(
                CommandHandler(f"article_{article_num}", self.article_command)
            )
        
        # Text message handler
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    def run(self):
        """Start the bot using polling mode."""
        # Create application
        self.application = Application.builder().token(self.bot_token).build()
        
        # Setup handlers
        self.setup_handlers()
        
        # Start polling
        print("🤖 Telegram bot started (polling mode)...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# Made with Bob
