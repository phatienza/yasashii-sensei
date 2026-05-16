---
name: yasashii-telegram
description: Format Yasashii Sensei Japanese lesson output for Telegram bot messages using proper Telegram markdown and inline keyboard buttons
---

Format Japanese lesson analysis results for Telegram bot messages
with inline keyboard buttons for navigation.

<Steps>
<Step>
Welcome message for /start command with inline keyboard buttons:

```
🎌 *Welcome to やさしい先生!*
_Your Gentle Japanese Teacher_

I help you understand Japanese text by providing:
📚 Vocabulary with readings
📖 Grammar explanations
🌐 English translation
🏯 Cultural notes
📊 JLPT difficulty level

*How to use:*
Just send me any Japanese text and I will analyze it!
```

Inline keyboard buttons below the message:
Row 1: [📰 Browse Articles] [🎲 Random Article]
Row 2: [❓ How to Use]

Use InlineKeyboardMarkup and InlineKeyboardButton.
Button callbacks:
- 📰 Browse Articles → callback_data="articles"
- 🎲 Random Article → callback_data="random"
- ❓ How to Use → callback_data="help"
</Step>

<Step>
Article list format for /articles command with inline buttons:

```
📰 *Today's Articles*
Choose an article to analyze:

1️⃣ 今日の天気 [N5 · lifestyle]
2️⃣ 東京で新しい美術館がオープン [N4 · culture]
3️⃣ 新しいスマートフォンアプリが人気 [N3 · technology]
4️⃣ 環境保護のための新しい政策が発表される [N2 · news]
5️⃣ 週末のカフェ巡り [N3 · lifestyle]
```

Inline keyboard buttons below:
Row 1: [1️⃣] [2️⃣] [3️⃣]
Row 2: [4️⃣] [5️⃣]

Button callbacks:
- [1️⃣] → callback_data="article_001"
- [2️⃣] → callback_data="article_002"
- [3️⃣] → callback_data="article_003"
- [4️⃣] → callback_data="article_004"
- [5️⃣] → callback_data="article_005"
</Step>

<Step>
Lesson header format:

```
🎌 *やさしい先生 Analysis*
📊 JLPT Level: *N4*
```
</Step>

<Step>
Vocabulary section format:

```
📚 *Vocabulary*

• 桜 (さくら) — cherry blossom [noun, N4]
• 見ごろ (みごろ) — best viewing time [noun, N3]
```
</Step>

<Step>
Grammar section format:

```
📖 *Grammar Patterns*

• *〜を迎えています* — reaching a peak or milestone
  Example: 桜が見ごろを迎えています
```

If no grammar patterns found, omit this section entirely.
</Step>

<Step>
Translation section format:

```
🌐 *Translation*
The cherry blossoms are at their best viewing season.
```
</Step>

<Step>
Cultural notes section format:

```
🏯 *Cultural Notes*

*Hanami:* The tradition of viewing cherry blossoms
is called Hanami (花見). People gather under sakura
trees for picnics and celebrations every spring.
```

If no cultural notes, omit this section entirely.
</Step>

<Step>
Footer with navigation buttons — always include after every lesson:

```
─────────────────
```

Inline keyboard buttons after every lesson:
Row 1: [📰 More Articles] [🎲 Random Article]
Row 2: [🏠 Home]

Button callbacks:
- 📰 More Articles → callback_data="articles"
- 🎲 Random Article → callback_data="random"
- 🏠 Home → callback_data="start"
</Step>

<Step>
Help message format for /help command:

```
❓ *やさしい先生 Commands*

💬 *[Japanese text]* — Analyze any Japanese text
📰 /articles — Browse today's sample articles
🔄 /start — Show welcome message
❓ /help — Show this help message

*Tips:*
• Works with any Japanese text
• Paste from manga, news, emails, signs
• Any JLPT level from N5 to N1
```

Inline keyboard buttons:
Row 1: [📰 Browse Articles] [🏠 Home]
</Step>

<Step>
Loading message — send before analysis starts:

```
🔍 *Analyzing Japanese text...*
This may take a few seconds ⏳
```

Always send bot.send_chat_action(chat_id, "typing")
before this message.
</Step>

<Step>
Error message format:

```
⚠️ *Analysis Error*

Sorry, I couldn't analyze that text right now.
Please try again in a moment.
```

Inline keyboard buttons:
Row 1: [🔄 Try Again] [🏠 Home]

Button callbacks:
- 🔄 Try Again → callback_data="retry"
- 🏠 Home → callback_data="start"
</Step>

<Step>
Not Japanese text message:

```
🤔 *That doesn't look like Japanese text*

Please send Japanese text for analysis.

*Examples of valid input:*
• Paste text from a Japanese website
• Copy from a Japanese app or game
• Type hiragana, katakana, or kanji
```

Inline keyboard buttons:
Row 1: [📰 Browse Articles] [🏠 Home]
</Step>
</Steps>

## Inline Keyboard Implementation

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Welcome screen buttons
def get_welcome_keyboard():
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

# Article selection buttons
def get_articles_keyboard():
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

# Post-lesson navigation buttons
def get_lesson_keyboard():
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
```

## Callback Query Handler

Register a CallbackQueryHandler to handle all button taps:
- "articles" → show article list with article keyboard
- "random" → pick random article and analyze it
- "help" → show help message
- "start" → show welcome message
- "article_001" to "article_005" → analyze that article
- "retry" → ask user to resend text

## Important Formatting Rules

- Use *text* for bold (Telegram Markdown)
- Use _text_ for italic
- Use • for bullet points
- Keep each message under 4096 characters
- Split into multiple messages if content exceeds limit
- Use emojis as section headers for visual clarity
- Never use HTML tags
- Use parse_mode='Markdown' not 'MarkdownV2' for simplicity
- Always attach inline keyboard to interactive messages

## Message Order For Lessons

1. Loading message with typing indicator
2. Header (JLPT level)
3. Vocabulary
4. Grammar (if present)
5. Translation
6. Cultural Notes (if present)
7. Navigation buttons (always)