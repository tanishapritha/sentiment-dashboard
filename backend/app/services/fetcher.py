import feedparser
import httpx
import pandas as pd
from app.config import REDDIT_RSS_URL, HN_API_URL, DEFAULT_LIMIT

async def fetch_reddit_rss(subreddit: str = "technology", limit: int = DEFAULT_LIMIT):
    url = REDDIT_RSS_URL.format(subreddit=subreddit)
    feed = feedparser.parse(url)
    data = [
        {"title": entry.title, "link": entry.link, "published": getattr(entry, 'published', 'N/A')}
        for entry in feed.entries[:limit]
    ]
    return pd.DataFrame(data)

async def fetch_hn_posts(query: str = "Python", limit: int = DEFAULT_LIMIT):
    url = HN_API_URL.format(query=query)
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
    res.raise_for_status()
    data_json = res.json()
    data = [
        {"title": post['title'], 
         "link": post.get('url', post.get('story_text', 'No link')),
         "published": post.get('created_at', 'N/A')}
        for post in data_json['hits'][:limit]
    ]
    return pd.DataFrame(data)
