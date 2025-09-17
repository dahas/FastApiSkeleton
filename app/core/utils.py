# Create utility functions here.

from fastapi import Depends, HTTPException, status
from app.core.models import User
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.locales.de import LangDe
from app.locales.en import LangEn

async def get_current_user(db: AsyncSession = Depends(get_db)):
    user_id = 1 # ToDo: Extract Identifier (id or email) from JWT or what you prefer.
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")
    return user

def get_lang(request):
    code = "en"
    if request is not None and hasattr(request, "headers") and request.headers:
        code = request.headers.get("Accept-Language", "en")[:2]
    if code.startswith("de"):
        return LangDe
    return LangEn