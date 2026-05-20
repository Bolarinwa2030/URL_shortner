import random 
import string
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.cache import redis_client
from app.models import URL
from pydantic import BaseModel, HttpUrl

router = APIRouter()

class URLCreate(BaseModel):
    original_url: HttpUrl
    custom_alias: str | None = None

def generate_short_code(length: int = 6) -> str:
    """Generate a random alphanumeric short code."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

@router.post("/shorten")
async def shorten_url(
    payload: URLCreate,
    db: Session = Depends(get_db)
):
    # Use custom alias or generate one
    short_code = payload.custom_alias or generate_short_code()

    # Check for collision in DB
    existing = db.query(URL).filter(URL.short_code == short_code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Short code already taken")

    url_obj = URL(short_code=short_code, original_url=str(payload.original_url))
    db.add(url_obj)
    db.commit()

    # Cache it immediately — first redirect will be fast
    redis_client.setex(short_code, 3600, str(payload.original_url))

    return {"short_url": f"https://yourdomain.com/{short_code}"}

@router.get("/{short_code}")
async def redirect_url(short_code: str, db: Session = Depends(get_db)):
    # 1. Check Redis first (fast path, ~0.1ms)
    cached = redis_client.get(short_code)
    if cached:
        return RedirectResponse(url=cached, status_code=302)

    # 2. Fall back to PostgreSQL (slow path, ~5ms)
    url_obj = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_obj:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # 3. Repopulate cache, increment click count
    redis_client.setex(short_code, 3600, url_obj.original_url)
    url_obj.click_count += 1
    db.commit()

    return RedirectResponse(url=url_obj.original_url, status_code=302)