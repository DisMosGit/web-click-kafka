from typing import Optional
from fastapi import Cookie, FastAPI, Header


async def get_user_id(
    token_header: Optional[str] = Header(default="", alias="Authorization"),
    token_cookie: Optional[str] = Cookie(default="", alias="Authorization"),
):
    if token_header:
        return int(token_header)
    elif token_cookie:
        return int(token_cookie)
    else:
        return None
