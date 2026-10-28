# Clash-inDepth-Royale

A web app that helps beginner Clash Royale players understand their game. Enter a
player tag and get a plain-language report:

- **Fix these first:** the three most important things to improve, each with what to do about it
- **Deck doctor:** checks the deck has a win condition, air defense, splash, spells and a tank answer, plus upgrade order
- **Battle review:** recent games with card-level comparison and the cards that keep beating you
- **Upcoming chests:** what's coming and when the good chests arrive

Data comes from the official [Clash Royale API](https://developer.clashroyale.com).

## Setup

Requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then paste your API key into .env
```

API keys are locked to the IP addresses you register on the developer site, so
create the key for the IP of the machine that runs the app.

## Run

```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000 and enter a player tag.

## Test

```bash
pytest
```

`scripts/test_api.py "#TAG"` checks your key and saves raw API responses to
`data/raw/` so you can see exactly what the API returns.

## Project layout

```
app/
  main.py          web routes
  cr_client.py     Clash Royale API client and tag validation
  storage.py       SQLite store that keeps every battle we've seen
  report.py        puts the analysis together for the page
  analysis/
    levels.py      converts API card levels to in-game levels
    cards.py       card roles and counter tips (hand-written)
    deck.py        deck doctor
    battles.py     battle results, patterns, nemesis cards
    coach.py       coaching rules that produce the tips
  templates/       Jinja pages
  static/          CSS
docs/              architecture, API notes, coaching rules, roadmap
scripts/           one-off tools
tests/
```

## Docs

- [Architecture](docs/ARCHITECTURE.md)
- [API notes](docs/API_NOTES.md): what the API returns and its quirks
- [Coaching rules](docs/COACHING_RULES.md): every tip the app can give and when
- [Roadmap](docs/ROADMAP.md)

Not affiliated with or endorsed by Supercell.
