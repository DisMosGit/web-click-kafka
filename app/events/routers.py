from typing import List

from fastapi import APIRouter, Depends

from app.auth.middlewares import get_user_id
from .models import Click

router = APIRouter(prefix="/events")


@router.post("/click")
async def registrate_click(click: Click.IN, user_id: int = Depends(get_user_id)):
    r = await Click.add(click, user_id)
    return {"ok": True, "count": r}
