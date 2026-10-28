"""Card level conversion.

The API stores levels per rarity (a max-level rare is `level 14, maxLevel 14`),
while the game shows one scale for every rarity. Adding the gap between the
card's maxLevel and the global max gives the level players see in the game.
"""

MAX_LEVEL = 16


def display_level(card: dict) -> int:
    return card["level"] + (MAX_LEVEL - card["maxLevel"])


def average_level(cards: list[dict]) -> float:
    if not cards:
        return 0.0
    return sum(display_level(c) for c in cards) / len(cards)
