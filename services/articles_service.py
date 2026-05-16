"""
Yasashii Sensei - Sample Articles Service
Hardcoded Japanese articles for demo (NHK Web Easy requires authentication).
"""

from typing import List, Optional, Dict, Any


# Hardcoded sample articles covering N5 to N2 difficulty levels
SAMPLE_ARTICLES = [
    {
        "id": "article_001",
        "title": "今日の天気",
        "content": "今日は天気がいいです。空が青くてきれいです。公園で友達と遊びました。とても楽しかったです。明日も晴れるといいですね。",
        "date": "2026-05-15",
        "difficulty": "N5",
        "topic": "lifestyle"
    },
    {
        "id": "article_002",
        "title": "東京で新しい美術館がオープン",
        "content": "東京の上野に新しい美術館がオープンしました。この美術館では、日本の伝統的な芸術作品と現代アートの両方を見ることができます。入場料は大人1000円、子供500円です。毎週月曜日は休館日です。",
        "date": "2026-05-14",
        "difficulty": "N4",
        "topic": "culture"
    },
    {
        "id": "article_003",
        "title": "新しいスマートフォンアプリが人気",
        "content": "日本語を勉強している外国人のための新しいアプリが登場しました。このアプリは、AIを使って文章を分析し、文法や語彙を説明してくれます。利用者からは「とても便利で分かりやすい」という声が多く聞かれます。無料でダウンロードできるので、興味がある人はぜひ試してみてください。",
        "date": "2026-05-13",
        "difficulty": "N3",
        "topic": "technology"
    },
    {
        "id": "article_004",
        "title": "環境保護のための新しい政策が発表される",
        "content": "政府は昨日、環境保護を強化するための新しい政策を発表しました。この政策により、2030年までに温室効果ガスの排出量を50%削減することを目指しています。専門家によると、この目標を達成するためには、再生可能エネルギーの利用拡大と、企業や個人の意識改革が不可欠だということです。環境問題への取り組みは、今後ますます重要になると予想されています。",
        "date": "2026-05-12",
        "difficulty": "N2",
        "topic": "news"
    },
    {
        "id": "article_005",
        "title": "週末のカフェ巡り",
        "content": "今日は友達と渋谷の新しいカフェに行ってきた！インスタ映えするラテアートが超かわいくて、思わず写真撮りまくっちゃった😊 ケーキも美味しかったし、店員さんも感じ良かった。また絶対行きたい！みんなもおすすめだよ〜",
        "date": "2026-05-15",
        "difficulty": "N3",
        "topic": "lifestyle"
    }
]


def get_articles() -> List[Dict[str, Any]]:
    """
    Get all sample articles.
    
    Returns:
        List of article dictionaries
    """
    return SAMPLE_ARTICLES


def get_article_by_id(article_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific article by ID.
    
    Args:
        article_id: Article ID (e.g., "article_001")
        
    Returns:
        Article dictionary if found, None otherwise
    """
    for article in SAMPLE_ARTICLES:
        if article["id"] == article_id:
            return article
    return None


def get_articles_by_difficulty(difficulty: str) -> List[Dict[str, Any]]:
    """
    Get articles filtered by JLPT difficulty level.
    
    Args:
        difficulty: JLPT level (N5, N4, N3, N2, N1)
        
    Returns:
        List of articles matching the difficulty level
    """
    return [article for article in SAMPLE_ARTICLES if article["difficulty"] == difficulty]


def get_articles_by_topic(topic: str) -> List[Dict[str, Any]]:
    """
    Get articles filtered by topic.
    
    Args:
        topic: Topic category (culture, news, lifestyle, technology, nature)
        
    Returns:
        List of articles matching the topic
    """
    return [article for article in SAMPLE_ARTICLES if article["topic"] == topic]


def get_article_count() -> int:
    """
    Get total number of sample articles.
    
    Returns:
        Number of articles
    """
    return len(SAMPLE_ARTICLES)


def get_available_difficulties() -> List[str]:
    """
    Get list of available difficulty levels.
    
    Returns:
        List of unique difficulty levels
    """
    return sorted(list(set(article["difficulty"] for article in SAMPLE_ARTICLES)))


def get_available_topics() -> List[str]:
    """
    Get list of available topics.
    
    Returns:
        List of unique topics
    """
    return sorted(list(set(article["topic"] for article in SAMPLE_ARTICLES)))

# Made with Bob
