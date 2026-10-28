import asyncio
import logging
import sqlite3
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import config
from .cr_client import ApiError, ClashClient, InvalidTag, PlayerNotFound, normalize_tag
from .report import build_report
from .storage import BattleStore

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=config.APP_DIR / "templates")

# tag -> (fetched_at, player, battles, chests)
_cache: dict[str, tuple] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = ClashClient(config.API_KEY, config.API_BASE_URL)
    try:
        app.state.store = BattleStore(config.DB_PATH)
    except (sqlite3.Error, OSError):
        logger.exception("Could not open battle store at %s; running without history", config.DB_PATH)
        app.state.store = None
    yield
    await app.state.client.aclose()


app = FastAPI(title="Clash-inDepth-Royale", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=config.APP_DIR / "static"), name="static")


def render_home(request: Request, error: str | None = None, tag: str = "", status: int = 200):
    return templates.TemplateResponse(
        request, "index.html", {"error": error, "tag": tag}, status_code=status
    )


async def fetch_player_data(client: ClashClient, tag: str):
    cached = _cache.get(tag)
    if cached and time.monotonic() - cached[0] < config.CACHE_SECONDS:
        return cached[1:]
    player, battles, chests = await asyncio.gather(
        client.get_player(tag), client.get_battlelog(tag), client.get_upcoming_chests(tag)
    )
    _cache[tag] = (time.monotonic(), player, battles, chests)
    return player, battles, chests


@app.get("/")
async def home(request: Request):
    return render_home(request)


@app.get("/lookup")
async def lookup(request: Request, tag: str = ""):
    try:
        clean = normalize_tag(tag)
    except InvalidTag:
        return render_home(request, "That doesn't look like a player tag. Tags use only the characters 0289PYLQGRJCUV.", tag, 400)
    return RedirectResponse(f"/player/{clean.lstrip('#')}", status_code=303)


@app.get("/player/{tag}")
async def player_report(request: Request, tag: str):
    try:
        clean = normalize_tag(tag)
    except InvalidTag:
        return render_home(request, "That doesn't look like a player tag.", tag, 400)
    if not config.API_KEY:
        return render_home(request, "The server has no API key. Add CR_API_KEY to the .env file.", tag, 500)

    try:
        player, battles, chests = await fetch_player_data(request.app.state.client, clean)
    except PlayerNotFound:
        return render_home(request, f"No player found with tag {clean}.", tag, 404)
    except ApiError as e:
        return render_home(request, str(e), tag, 502)

    store: BattleStore | None = request.app.state.store
    if store:
        try:
            store.save(clean, battles)
            battles = store.recent(clean)
        except sqlite3.Error:
            # Saved history is a bonus; the report still works from the API's battles.
            logger.exception("Battle store unavailable")
    report = build_report(player, battles, chests)
    return templates.TemplateResponse(request, "report.html", {"r": report})


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse("/static/favicon.svg", status_code=307)


@app.get("/health")
async def health():
    return {"ok": True}
