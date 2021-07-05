import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()
print(os.environ.get("ENV_FILE"))
load_dotenv(os.environ.get("ENV_FILE"))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT")),
        log_level=os.environ.get("LOG_LEVEL"),
        debug=bool(os.environ.get("DEBUG")),
    )
