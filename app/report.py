"""Builds the full player report from raw API data."""

from dataclasses import dataclass

from .analysis.battles import BattleSummary, summarize
from .analysis.coach import Tip, coach
from .analysis.deck import DeckReport, analyze_deck

# Rewards worth pointing out in the chest preview.
SPECIAL_CHESTS = ("Legendary", "Epic", "Mega Lightning", "Royal Wild", "Magical", "Giant", "Tower Troop", "Overflowing")


@dataclass
class ChestPreview:
    name: str
    in_chests: int
    special: bool


@dataclass
class Report:
    player: dict
    deck: DeckReport
    summary: BattleSummary
    tips: list[Tip]
    chests: list[ChestPreview]

    @property
    def top_tips(self) -> list[Tip]:
        return self.tips[:3]

    @property
    def more_tips(self) -> list[Tip]:
        return self.tips[3:]


def chest_preview(items: list[dict]) -> list[ChestPreview]:
    return [
        ChestPreview(c["name"], c["index"], any(s in c["name"] for s in SPECIAL_CHESTS))
        for c in items
    ]


def build_report(player: dict, raw_battles: list[dict], chests: list[dict]) -> Report:
    deck_cards = player.get("currentDeck", [])
    deck = analyze_deck(deck_cards)
    summary = summarize(raw_battles, {c["name"] for c in deck_cards})
    return Report(player, deck, summary, coach(deck, summary), chest_preview(chests))
