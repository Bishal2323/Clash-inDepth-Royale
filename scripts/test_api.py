"""Smoke test for the Clash Royale API.

Fetches a player's profile, battle log and upcoming chests, saves the raw JSON
to data/raw/, and prints a short summary of which fields are available.

Usage: python3 scripts/test_api.py "#PV20Q9QQ8"
"""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://api.clashroyale.com/v1"


def load_api_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("CR_API_KEY="):
            key = line.split("=", 1)[1].strip()
            if key:
                return key
    sys.exit("CR_API_KEY is empty in .env. Paste your key there first.")


def get(path, key):
    req = urllib.request.Request(
        BASE_URL + path,
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"  {path} -> HTTP {e.code}: {body[:300]}")
        return None


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "#PV20Q9QQ8"
    tag = "#" + tag.upper().lstrip("#").replace("O", "0")
    encoded = urllib.parse.quote(tag)
    key = load_api_key()

    out_dir = ROOT / "data" / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)

    endpoints = {
        "player": f"/players/{encoded}",
        "battlelog": f"/players/{encoded}/battlelog",
        "upcomingchests": f"/players/{encoded}/upcomingchests",
    }
    results = {}
    for name, path in endpoints.items():
        data = get(path, key)
        results[name] = data
        if data is not None:
            (out_dir / f"{name}.json").write_text(json.dumps(data, indent=2))
            print(f"  {name}: OK (saved to data/raw/{name}.json)")

    player = results["player"]
    if player:
        print(f"\nPlayer: {player.get('name')} {player.get('tag')}")
        print(f"  Trophies {player.get('trophies')} (best {player.get('bestTrophies')}), "
              f"arena {player.get('arena', {}).get('name')}, King level {player.get('expLevel')}")
        print(f"  Wins {player.get('wins')} / losses {player.get('losses')}, "
              f"3-crown wins {player.get('threeCrownWins')}")
        print(f"  Cards owned: {len(player.get('cards', []))}, "
              f"current deck: {[c['name'] for c in player.get('currentDeck', [])]}")
        print(f"  Profile fields: {sorted(player.keys())}")

    battles = results["battlelog"]
    if battles:
        print(f"\nBattles returned: {len(battles)}")
        first = battles[0]
        print(f"  Battle fields: {sorted(first.keys())}")
        print(f"  Team member fields: {sorted(first['team'][0].keys())}")
        modes = {}
        for b in battles:
            modes[b.get("type")] = modes.get(b.get("type"), 0) + 1
        print(f"  Battle types: {modes}")

    chests = results["upcomingchests"]
    if chests is not None:
        print(f"\nUpcoming chests: {json.dumps(chests)[:300]}")


if __name__ == "__main__":
    main()
