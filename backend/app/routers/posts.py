from fastapi import APIRouter, Query
import pandas as pd
from fastapi.responses import JSONResponse
from app.models.post import Post
from app.services import fetch_reddit_rss, fetch_hn_posts, clean_text, analyze_sentiment

router = APIRouter()

@router.get("/posts", response_model=list[Post], summary="Fetch Reddit & Hacker News posts")
async def get_all_posts(
    subreddit: str = Query("technology", description="Reddit subreddit to fetch posts from"),
    query: str = Query("Python", description="Hacker News search query"),
    limit: int = Query(20, description="Number of posts to fetch from each source")
):
    try:
        # Fetch data
        df_reddit = await fetch_reddit_rss(subreddit=subreddit, limit=limit)
        df_hn = await fetch_hn_posts(query=query, limit=limit)
        df_all = pd.concat([df_reddit, df_hn], ignore_index=True)

        # Preprocess and analyze sentiment
        df_all['cleaned'] = df_all['title'].apply(clean_text)
        df_all['sentiment'] = df_all['cleaned'].apply(analyze_sentiment)

        # Convert to dict
        posts = df_all.to_dict(orient='records')

        # Return standardized JSON
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "code": 200,
                "data": posts
            }
        )

    except Exception as e:
        # Return friendly error JSON
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "code": 500,
                "message": "An error occurred while fetching or processing posts.",
                "details": str(e)
            }
        )
