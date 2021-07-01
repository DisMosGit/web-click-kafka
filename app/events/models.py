from typing import Optional
import orjson, pydantic

class Click(pydantic.BaseModel):
    x: float
    y: float
    window_x: int
    window_y: int
    duration: Optional[int]
    page: str
    user_id: Optional[int]

class Word(pydantic.BaseModel):
    value: str
    duration: Optional[int]
    page: str
    user_id: Optional[int]

class Following(pydantic.BaseModel):
    from_page: str
    to_page: str
    delay: int
    user_id: Optional[int]