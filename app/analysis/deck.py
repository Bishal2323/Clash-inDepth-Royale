"""Deck Doctor: checks a deck for missing roles, cost and card levels."""

from dataclasses import dataclass, field

from .cards import ROLE_SETS
from .levels import display_level

# (role key, label shown to the player, how many cards a deck should have, hint)
ROLE_REQUIREMENTS = [
    ("win_condition", "Win condition", 1, "A card whose job is to damage towers, like Hog Rider or Giant."),
    ("air_defense", "Air defense", 2, "Cards that can hit flying troops. Two is safer than one."),
    ("splash", "Splash damage", 1, "Hits groups of troops at once, like Valkyrie or Baby Dragon."),
    ("small_spell", "Small spell", 1, "Cheap spell for swarms, like Zap, The Log or Arrows."),
    ("big_spell", "Big spell", 1, "Kills medium troops or finishes towers, like Fireball or Poison."),
    ("tank_answer", "Tank killer or building", 1, "Stops big troops, like Mini P.E.K.K.A, Inferno Tower or Cannon."),
]

HEAVY_DECK = 4.3
LIGHT_DECK = 2.7


@dataclass
class RoleCheck:
    key: str
    label: str
    hint: str
    needed: int
    cards: list[str]

    @property
    def ok(self) -> bool:
        return len(self.cards) >= self.needed


@dataclass
class DeckCard:
    name: str
    level: int
    elixir: int
    icon: str | None
    evolved: bool


@dataclass
class DeckReport:
    cards: list[DeckCard]
    avg_elixir: float
    roles: list[RoleCheck]
    # Cards below the deck's best level, biggest gap first: (card, levels behind).
    upgrade_priority: list[tuple[DeckCard, int]] = field(default_factory=list)

    def role(self, key: str) -> RoleCheck:
        return next(r for r in self.roles if r.key == key)

    @property
    def missing_roles(self) -> list[RoleCheck]:
        return [r for r in self.roles if not r.ok]


def analyze_deck(api_cards: list[dict]) -> DeckReport:
    cards = []
    for c in api_cards:
        evolved = c.get("evolutionLevel", 0) > 0
        icons = c.get("iconUrls", {})
        cards.append(DeckCard(
            name=c["name"],
            level=display_level(c),
            elixir=c.get("elixirCost", 0),
            icon=icons.get("evolutionMedium") if evolved else icons.get("medium"),
            evolved=evolved,
        ))

    names = [c.name for c in cards]
    roles = [
        RoleCheck(key, label, hint, needed, [n for n in names if n in ROLE_SETS[key]])
        for key, label, needed, hint in ROLE_REQUIREMENTS
    ]
    costed = [c.elixir for c in cards if c.elixir]
    avg_elixir = round(sum(costed) / len(costed), 2) if costed else 0.0

    top = max((c.level for c in cards), default=0)
    behind = sorted(((c, top - c.level) for c in cards if c.level < top), key=lambda x: -x[1])
    return DeckReport(cards, avg_elixir, roles, behind)
