from typing import List

from fastapi import Response, Request, APIRouter, Depends

from app.auth.middlewares import get_user_id
from .models import Click, Word, Following

router = APIRouter(prefix="/events")


@router.post("/click", response_model=List[Click])
async def registrate_click(click: Click, user_id: int = Depends(get_user_id)):
    click.user_id = user_id
    return click
