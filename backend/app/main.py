from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers import posts

app = FastAPI(
    title="Real-Time Sentiment Dashboard",
    description="Fetch Reddit and Hacker News posts, preprocess, and analyze sentiment in real-time.",
    version="1.0.0",
)

# Include routers
app.include_router(posts.router, prefix="/api", tags=["Posts"])

# Root endpoint
@app.get("/", summary="API Root")
def root():
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "code": 200,
            "message": "Welcome to the Real-Time Sentiment Dashboard API",
            "endpoints": {
                "get_posts": "/api/posts?subreddit=technology&query=Python&limit=20"
            }
        }
    )

# Custom 404 handler
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "code": 404,
            "message": f"Oops! The requested endpoint {request.url.path} was not found."
        },
    )

# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "code": 422,
            "message": "Invalid input parameters",
            "details": exc.errors()
        }
    )
