# Sample Articles Specification

**Purpose**: Define the 5 hardcoded Japanese articles for the Yasashii Sensei application.

**Context**: NHK Web Easy requires authentication and cannot be accessed programmatically. These curated sample articles will be displayed as "Today's Articles" in both the web UI and Telegram bot.

---

## Article Structure

Each article must have:
- `id` (string): Unique identifier (e.g., "article_001")
- `title` (string): Japanese title
- `content` (string): Japanese content (3-5 sentences)
- `date` (string): Publication date in ISO format (YYYY-MM-DD)
- `difficulty` (string): JLPT level (N5, N4, N3, N2, or N1)
- `topic` (string): Category tag (culture, news, lifestyle, technology, nature)

---

## Article 1: Beginner (N5) - Daily Life

```python
{
    "id": "article_001",
    "title": "今日の天気",
    "content": "今日は天気がいいです。空が青くてきれいです。公園で友達と遊びました。とても楽しかったです。明日も晴れるといいですね。",
    "date": "2026-05-15",
    "difficulty": "N5",
    "topic": "lifestyle"
}
```

**Vocabulary**: 天気 (weather), 空 (sky), 青い (blue), 公園 (park), 友達 (friend), 遊ぶ (play), 楽しい (fun), 明日 (tomorrow), 晴れる (sunny)

**Grammar**: です/でした (polite form), と (with), で (location particle), といい (hope/wish)

---

## Article 2: Elementary (N4) - Culture

```python
{
    "id": "article_002",
    "title": "東京で新しい美術館がオープン",
    "content": "東京の上野に新しい美術館がオープンしました。この美術館では、日本の伝統的な芸術作品と現代アートの両方を見ることができます。入場料は大人1000円、子供500円です。毎週月曜日は休館日です。",
    "date": "2026-05-14",
    "difficulty": "N4",
    "topic": "culture"
}
```

**Vocabulary**: 美術館 (art museum), オープン (open), 伝統的 (traditional), 芸術作品 (artwork), 現代アート (modern art), 両方 (both), 入場料 (admission fee), 休館日 (closed day)

**Grammar**: 〜で (location), 〜ました (past tense), 〜では (topic marker), 〜ことができます (can do), 〜は〜です (A is B)

---

## Article 3: Intermediate (N3) - Technology

```python
{
    "id": "article_003",
    "title": "新しいスマートフォンアプリが人気",
    "content": "日本語を勉強している外国人のための新しいアプリが登場しました。このアプリは、AIを使って文章を分析し、文法や語彙を説明してくれます。利用者からは「とても便利で分かりやすい」という声が多く聞かれます。無料でダウンロードできるので、興味がある人はぜひ試してみてください。",
    "date": "2026-05-13",
    "difficulty": "N3",
    "topic": "technology"
}
```

**Vocabulary**: アプリ (app), 勉強する (study), 外国人 (foreigner), 登場する (appear/launch), 分析する (analyze), 文法 (grammar), 語彙 (vocabulary), 説明する (explain), 利用者 (user), 便利 (convenient), 無料 (free), ダウンロード (download)

**Grammar**: 〜ている (ongoing state), 〜ための (for the purpose of), 〜を使って (using), 〜てくれます (do for someone), 〜という (quotation), 〜から (from), 〜ので (because), 〜てみてください (please try)

---

## Article 4: Upper Intermediate (N2) - News

```python
{
    "id": "article_004",
    "title": "環境保護のための新しい政策が発表される",
    "content": "政府は昨日、環境保護を強化するための新しい政策を発表しました。この政策により、2030年までに温室効果ガスの排出量を50%削減することを目指しています。専門家によると、この目標を達成するためには、再生可能エネルギーの利用拡大と、企業や個人の意識改革が不可欠だということです。環境問題への取り組みは、今後ますます重要になると予想されています。",
    "date": "2026-05-12",
    "difficulty": "N2",
    "topic": "news"
}
```

**Vocabulary**: 環境保護 (environmental protection), 政策 (policy), 発表する (announce), 強化する (strengthen), 温室効果ガス (greenhouse gas), 排出量 (emissions), 削減 (reduction), 目指す (aim for), 専門家 (expert), 達成する (achieve), 再生可能エネルギー (renewable energy), 利用拡大 (expansion of use), 意識改革 (awareness reform), 不可欠 (indispensable), 取り組み (efforts), 予想される (expected)

**Grammar**: 〜ための (for the purpose of), 〜により (by means of), 〜までに (by the time), 〜ことを目指す (aim to do), 〜によると (according to), 〜ためには (in order to), 〜が不可欠だ (is essential), 〜への (toward), 〜ますます (more and more), 〜と予想される (is expected that)

---

## Article 5: Casual/Social Media Style (N3-N2)

```python
{
    "id": "article_005",
    "title": "週末のカフェ巡り",
    "content": "今日は友達と渋谷の新しいカフェに行ってきた！インスタ映えするラテアートが超かわいくて、思わず写真撮りまくっちゃった😊 ケーキも美味しかったし、店員さんも感じ良かった。また絶対行きたい！みんなもおすすめだよ〜",
    "date": "2026-05-15",
    "difficulty": "N3",
    "topic": "lifestyle"
}
```

**Vocabulary**: 週末 (weekend), カフェ巡り (cafe hopping), 渋谷 (Shibuya), インスタ映え (Instagram-worthy), ラテアート (latte art), 超 (super), かわいい (cute), 思わず (unintentionally), 撮る (take photo), 店員 (staff), 感じ (feeling/impression), 絶対 (definitely), おすすめ (recommend)

**Grammar**: 〜てきた (went and came back), 〜する (casual form), 〜くて (and), 〜ちゃった (ended up doing), 〜し (and also), 〜たい (want to), 〜だよ (casual assertion), 〜も (also)

**Note**: This article demonstrates casual Japanese with:
- Casual verb forms (行ってきた instead of 行ってきました)
- Slang (超, インスタ映え)
- Emoji usage (😊)
- Casual sentence endings (〜だよ, 〜ちゃった)
- Colloquial expressions

---

## Implementation Notes

### In `services/articles_service.py`:

```python
SAMPLE_ARTICLES = [
    {
        "id": "article_001",
        "title": "今日の天気",
        "content": "今日は天気がいいです。空が青くてきれいです。公園で友達と遊びました。とても楽しかったです。明日も晴れるといいですね。",
        "date": "2026-05-15",
        "difficulty": "N5",
        "topic": "lifestyle"
    },
    # ... (articles 2-5)
]

def get_articles():
    """Return all sample articles"""
    return SAMPLE_ARTICLES

def get_article_by_id(article_id):
    """Get a specific article by ID"""
    for article in SAMPLE_ARTICLES:
        if article["id"] == article_id:
            return article
    return None
```

### Display in UI:

- Show as "Today's Articles" (今日の記事)
- Display with difficulty badge (N5-N2)
- Show topic tag
- One-click to analyze

### Display in Telegram Bot:

- `/articles` command shows list
- User can select by number (1-5)
- Article auto-loads for analysis

---

## Rationale for Article Selection

1. **Article 1 (N5)**: Simple daily life content for absolute beginners
2. **Article 2 (N4)**: Cultural topic with basic grammar structures
3. **Article 3 (N3)**: Technology topic relevant to the app itself (meta)
4. **Article 4 (N2)**: Formal news style with complex grammar
5. **Article 5 (Casual)**: Social media style to show real-world Japanese

This selection covers:
- ✅ Multiple difficulty levels (N5 to N2)
- ✅ Diverse topics (lifestyle, culture, technology, news)
- ✅ Different writing styles (formal, casual, social media)
- ✅ Realistic content length (3-5 sentences)
- ✅ Authentic Japanese usage

---

## Future Expansion

If time permits, additional articles can be added for:
- N1 level content (academic/business Japanese)
- Seasonal topics (holidays, weather)
- Regional dialects
- Historical content
- Scientific topics

However, 5 articles are sufficient for the MVP demo.