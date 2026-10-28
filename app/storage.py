"""Keeps every battle we have seen, since the API only returns the latest ~30."""

import json
import sqlite3
from contextlib import closing
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS battles (
    player_tag  TEXT NOT NULL,
    battle_time TEXT NOT NULL,
    battle_type TEXT,
    raw         TEXT NOT NULL,
    PRIMARY KEY (player_tag, battle_time)
)
"""


class BattleStore:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._path = path
        with self._connect() as conn:
            conn.execute(SCHEMA)

    def _connect(self):
        return closing(sqlite3.connect(self._path))

    def save(self, tag: str, battles: list[dict]):
        rows = [(tag, b["battleTime"], b.get("type"), json.dumps(b)) for b in battles]
        with self._connect() as conn, conn:
            conn.executemany("INSERT OR IGNORE INTO battles VALUES (?, ?, ?, ?)", rows)

    def recent(self, tag: str, limit: int = 100) -> list[dict]:
        """Newest first. battleTime strings like 20261028T201103.000Z sort correctly as text."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT raw FROM battles WHERE player_tag = ? ORDER BY battle_time DESC LIMIT ?",
                (tag, limit),
            ).fetchall()
        return [json.loads(r[0]) for r in rows]
