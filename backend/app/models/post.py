from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    link: str
    published: Optional[str]
    cleaned: Optional[str] = None
    sentiment: Optional[str] = None
