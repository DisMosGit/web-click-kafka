import os

import pytest
from httpx import AsyncClient
from dotenv import load_dotenv

from app.main import app

load_dotenv()
load_dotenv(os.environ.get("ENV_FILE"))


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health-check")
    assert response.status_code == 200
    assert response.json().get("ok") == True
