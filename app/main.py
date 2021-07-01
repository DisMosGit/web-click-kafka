import os

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Python",
    debug=bool(os.environ.get('DEBUG')),
    version=os.environ.get('APP_VERSION'),
    default_response_class=ORJSONResponse,
    openapi_url=os.environ.get('SWAGGER_URL'),
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def health_check():
    return {"ok": True, "version": app.version}


from app.events.routers import router as events

app.include_router(events, prefix="/api")
