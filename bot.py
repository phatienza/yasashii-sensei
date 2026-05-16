#!/usr/bin/env python3
"""
Yasashii Sensei - Standalone Telegram Bot Entry Point
Run this file to start the Telegram bot independently from Flask.

Usage:
    python bot.py

Requirements:
    - TELEGRAM_BOT_TOKEN in .env
    - WATSONX_API_KEY in .env
    - WATSONX_PROJECT_ID in .env
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services
from services.watsonx_service import WatsonxService
from services.telegram_service import TelegramService


def validate_environment():
    """
    Validate required environment variables are set.
    
    Raises:
        ValueError: If required variables are missing
    """
    required_vars = [
        "TELEGRAM_BOT_TOKEN",
        "WATSONX_API_KEY",
        "WATSONX_PROJECT_ID"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please set them in your .env file."
        )


def main():
    """Main entry point for standalone Telegram bot."""
    
    print("=" * 60)
    print("🌸 Yasashii Sensei - Telegram Bot")
    print("=" * 60)
    
    try:
        # Validate environment
        print("\n📋 Validating environment variables...")
        validate_environment()
        print("✅ Environment variables validated")
        
        # Get configuration from environment
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        watsonx_api_key = os.getenv("WATSONX_API_KEY")
        watsonx_project_id = os.getenv("WATSONX_PROJECT_ID")
        watsonx_url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        
        # Initialize watsonx.ai service
        print("\n🤖 Initializing watsonx.ai service...")
        watsonx_service = WatsonxService(
            api_key=watsonx_api_key,
            project_id=watsonx_project_id,
            url=watsonx_url
        )
        
        model_info = watsonx_service.get_model_info()
        print(f"✅ watsonx.ai initialized")
        print(f"   Primary model: {model_info['primary_model']}")
        print(f"   Fallback model: {model_info['fallback_model']}")
        
        # Initialize Telegram service
        print("\n📱 Initializing Telegram bot service...")
        telegram_service = TelegramService(
            bot_token=telegram_token,
            watsonx_service=watsonx_service
        )
        print("✅ Telegram service initialized")
        
        # Start bot
        print("\n" + "=" * 60)
        print("🚀 Starting Telegram bot (polling mode)...")
        print("=" * 60)
        print("\n💡 Bot is now running. Press Ctrl+C to stop.\n")
        
        telegram_service.run()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Bot stopped by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check your .env file has all required variables")
        print("   2. Verify your Telegram bot token from BotFather")
        print("   3. Verify your watsonx.ai credentials")
        print("   4. Check your internet connection")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
