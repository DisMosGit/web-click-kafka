from typing import Optional
from uuid import UUID
from random import choice
from fastapi import Cookie, FastAPI, Header

users = [
    UUID("8b100004-4028-4189-8c35-90add571a8b0"),
    UUID("58401743-124c-45cc-ac1b-3aebb002e443"),
    UUID("c951f24b-7abb-4f24-b7f9-2f9ca7542c98"),
    UUID("5a2a2efc-675d-4d84-91cd-311e2279fea0"),
    UUID("70aa0b10-f1c0-4d7a-816b-381c2117e7b4"),
    UUID("8776959f-f3c1-4aa8-8ea6-cc4e5e99410e"),
    UUID("5806333a-6223-4bca-bed6-8ef0eaa9e063"),
    UUID("f0fdab87-d704-4069-a8b9-1d969d7a07d6"),
    UUID("71b970cb-6696-4d03-8d0d-eaf630e98231"),
    UUID("a0a6cdfe-cce2-410a-864f-fdd5143e3149"),
]


async def get_user_id():
    return choice(users + [None, None, None])
