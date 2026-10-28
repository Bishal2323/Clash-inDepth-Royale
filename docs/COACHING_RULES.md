# Coaching rules

All rules live in `app/analysis/coach.py`. Each returns one tip or nothing.
Tips are sorted by severity (high → medium → low); the first three are shown as
"Fix these first", the rest under "more tips".

Thresholds are starting values. Tune them as we look at more players.

## Deck rules (current deck)

| Rule | Fires when | Severity |
|---|---|---|
| `no_win_condition` | No card from `WIN_CONDITIONS` | high |
| `weak_air_defense` | Fewer than 2 cards that hit air | high if 0, medium if 1 |
| `no_small_spell` | No Zap / Log / Arrows / Snowball / ... | medium |
| `no_splash` | No splash damage card | medium |
| `no_tank_answer` | No building and no tank killer | medium |
| `no_big_spell` | No Fireball / Poison / Rocket / Lightning / Void | low |
| `deck_cost` | Average elixir > 4.3 (medium) or < 2.7 (low) | medium / low |
| `underleveled_cards` | A deck card is behind the deck's best level | high if ≥2 behind, else low |

## Battle rules (stored battles, friendlies and 2v2 excluded)

| Rule | Fires when | Severity |
|---|---|---|
| `outleveled_losses` | ≥2 losses where the opponent's cards averaged ≥1.5 levels higher | high |
| `nemesis_card` | A card was in ≥3 losses and ≥40% of losses | medium |
| `three_crowned` | ≥3 three-crown losses and ≥30% of losses | medium |
| `close_losses` | ≥4 losses and at least half were by one crown | low |

Losses with elixir leaked ≥12 are labeled "possible disconnect" and don't count
toward nemesis cards or 3-crown losses.

## Not used on purpose

**Elixir leaked.** It's a single number per match, waiting can be correct, and
we can't see why it happened. It stays out of the tips.

## Adding a rule

```python
@rule
def my_rule(deck, summary):
    if <nothing wrong>:
        return None
    return Tip(MEDIUM, "Short title", "Why it matters, with the player's numbers.", "What to do.")
```

Add a test in `tests/test_analysis.py` and a row in this file.
