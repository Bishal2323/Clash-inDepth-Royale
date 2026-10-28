# Architecture

## Request flow

```
Browser ── GET /lookup?tag=... ──► normalize tag ──► redirect /player/{TAG}
Browser ── GET /player/{TAG}
             │
             ├─ fetch_player_data()  (2-minute in-memory cache)
             │     ├─ GET /players/{tag}
             │     ├─ GET /players/{tag}/battlelog        (in parallel)
             │     └─ GET /players/{tag}/upcomingchests
             │
             ├─ BattleStore.save()     keep new battles in SQLite
             ├─ BattleStore.recent()   up to 100 stored battles, newest first
             │
             ├─ build_report()
             │     ├─ analyze_deck(currentDeck)   → DeckReport
             │     ├─ summarize(battles)          → BattleSummary
             │     └─ coach(deck, summary)        → sorted list of Tips
             │
             └─ render report.html
```

## Decisions

**Server-rendered pages (FastAPI + Jinja).** Everything stays in Python, with no
frontend build step. If the pages need more interactivity we can add HTMX or move
to a separate frontend later; the analysis code doesn't depend on the web layer.

**Analysis is plain functions over API dicts.** `app/analysis/` never calls the
API or the database, so it is easy to test with fake data (`tests/helpers.py`).

**Store every battle.** The API only returns the latest ~30 battles. Saving them
in SQLite (`data/clashroy.db`) lets the report grow with each visit and enables
progress tracking later.

**Coaching is rule-based.** Each rule in `coach.py` is a small function that
returns a `Tip` or nothing. Rules are predictable, easy to test and easy to add.
An LLM could later rewrite the wording, but the rules decide *what* is said.

**Card knowledge is hand-written.** The API doesn't say what a card does (hits
air, splash, building...). `cards.py` holds those sets and needs updating when
new cards are released.

## Secrets

The API key lives only in `.env` (git-ignored) and is read by `app/config.py`.
