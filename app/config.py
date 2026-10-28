import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "app"

load_dotenv(ROOT / ".env")

API_KEY = os.getenv("CR_API_KEY", "").strip()
API_BASE_URL = os.getenv("CR_API_BASE_URL", "https://api.clashroyale.com/v1").rstrip("/")
DB_PATH = Path(os.getenv("CR_DB_PATH", ROOT / "data" / "clashroy.db"))

# How long a player's API responses are reused before we call the API again.
CACHE_SECONDS = 120
