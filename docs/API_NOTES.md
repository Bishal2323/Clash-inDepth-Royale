# Clash Royale API notes

Base URL: `https://api.clashroyale.com/v1`. Auth: `Authorization: Bearer <key>`.
Tags must be URL-encoded (`#` → `%23`).

Checked against real responses on 2026-10-28.

## Endpoints we use

### `GET /players/{tag}`
Profile: `name`, `tag`, `trophies`, `bestTrophies`, `arena`, `expLevel`, `wins`,
`losses`, `threeCrownWins`, `clan`, `currentDeck`, `currentDeckSupportCards`,
`cards` (whole collection), `currentWinLoseStreak`, Path of Legend results
(`currentPathOfLegendSeasonResult`, ...), `leagueStatistics`, `badges`,
`achievements`, `progress` (other game modes' trophy roads).

### `GET /players/{tag}/battlelog`
The latest ~30 battles. Each has `type` (`pathOfLegend`, `PvP`, `friendly`, ...),
`battleTime` (`20261028T201103.000Z`, UTC), `gameMode`, `arena`, and `team` /
`opponent` lists. Each player entry has:

| Field | Notes |
|---|---|
| `cards` | Deck with `level`, `maxLevel`, `evolutionLevel`, `elixirCost`, icons |
| `crowns` | Crowns earned |
| `trophyChange` | Missing in some modes |
| `kingTowerHitPoints`, `princessTowersHitPoints` | HP left at the end; destroyed towers are missing |
| `elixirLeaked` | Total for the match only (see below) |
| `supportCards` | Tower troop |

2v2 battles have two entries in `team`; we skip those for now.

### `GET /players/{tag}/upcomingchests`
`{"items": [{"index": 0, "name": "Golden Chest"}, ...]}`. Index is how many
chests away it is. Also lists far-off special chests (e.g. Legendary Chest at 55).

## Quirks

- **Card levels are per rarity.** A max rare is `level: 14, maxLevel: 14`. The
  in-game level is `level + (16 - maxLevel)` (see `analysis/levels.py`).
- **`elixirLeaked` is a match total.** We don't know when or why it leaked, and
  sometimes waiting is the right play. We don't base tips on it; we only use very
  high values (≥12) to label a loss as a possible disconnect.
- **No placement, timing or replay data.** Placement analysis would need video
  (see roadmap).
- **Keys are IP-locked.** Deploying needs a key for the server's IP, or the
  RoyaleAPI proxy (`CR_API_BASE_URL` in `.env`).
- Errors: 403 = bad key or IP, 404 = unknown tag, 429 = rate limited,
  503 = maintenance.
