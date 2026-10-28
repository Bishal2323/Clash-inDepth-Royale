"""Turns raw battle log entries into results and patterns."""

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .levels import average_level

MODE_LABELS = {
    "pathOfLegend": "Ranked",
    "PvP": "Ladder",
    "friendly": "Friendly",
    "challenge": "Challenge",
    "tournament": "Tournament",
    "clanWarWarDay": "Clan War",
    "riverRacePvP": "River Race",
    "riverRaceDuel": "River Race Duel",
    "riverRaceDuelColosseum": "Colosseum Duel",
    "boatBattle": "Boat Battle",
    "trail": "Event",
}

# Practice games and boat battles say nothing about how the player is doing.
IGNORED_TYPES = {"friendly", "boatBattle"}

# A leak this big usually means the player disconnected or stopped playing,
# not a skill problem, so we label the game instead of judging it.
AFK_LEAK = 12

# A level gap at least this big makes a match very hard to win.
BIG_LEVEL_GAP = 1.5


@dataclass
class Battle:
    time: datetime
    mode: str
    result: str  # "win", "loss" or "draw"
    my_crowns: int
    opp_crowns: int
    trophy_change: int | None
    my_cards: list[str]
    my_level: float
    opp_name: str
    opp_cards: list[str]
    opp_level: float
    elixir_leaked: float | None
    used_main_deck: bool
    # (name, icon url) for showing the opponent's deck.
    opp_deck: list[tuple[str, str | None]] = field(default_factory=list)

    @property
    def level_gap(self) -> float:
        """Positive when the opponent's cards are higher level."""
        return self.opp_level - self.my_level

    @property
    def possible_afk(self) -> bool:
        return self.result == "loss" and (self.elixir_leaked or 0) >= AFK_LEAK

    @property
    def close(self) -> bool:
        return abs(self.my_crowns - self.opp_crowns) == 1


@dataclass
class Nemesis:
    card: str
    losses_with: int
    games_with: int
    icon: str | None = None


@dataclass
class BattleSummary:
    battles: list[Battle]
    wins: int = 0
    losses: int = 0
    draws: int = 0
    close_losses: int = 0
    three_crown_losses: int = 0
    big_gap_losses: list[Battle] = field(default_factory=list)
    nemeses: list[Nemesis] = field(default_factory=list)

    @property
    def games(self) -> int:
        return len(self.battles)

    @property
    def win_rate(self) -> float:
        return self.wins / self.games if self.games else 0.0


def parse_battle_time(value: str) -> datetime:
    return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc)


def parse_battle(raw: dict, main_deck: set[str]) -> Battle | None:
    """Returns None for battles we don't analyze (friendlies, 2v2)."""
    if raw.get("type") in IGNORED_TYPES or len(raw.get("team", [])) != 1:
        return None
    me, opp = raw["team"][0], raw["opponent"][0]
    my_crowns, opp_crowns = me.get("crowns", 0), opp.get("crowns", 0)
    result = "win" if my_crowns > opp_crowns else "loss" if my_crowns < opp_crowns else "draw"
    my_cards = [c["name"] for c in me["cards"]]
    return Battle(
        time=parse_battle_time(raw["battleTime"]),
        mode=MODE_LABELS.get(raw.get("type"), raw.get("type", "Other")),
        result=result,
        my_crowns=my_crowns,
        opp_crowns=opp_crowns,
        trophy_change=me.get("trophyChange"),
        my_cards=my_cards,
        my_level=round(average_level(me["cards"]), 1),
        opp_name=opp.get("name", "?"),
        opp_cards=[c["name"] for c in opp["cards"]],
        opp_level=round(average_level(opp["cards"]), 1),
        elixir_leaked=me.get("elixirLeaked"),
        used_main_deck=set(my_cards) == main_deck,
        opp_deck=[(c["name"], c.get("iconUrls", {}).get("medium")) for c in opp["cards"]],
    )


def summarize(raw_battles: list[dict], main_deck: set[str]) -> BattleSummary:
    battles = [b for b in (parse_battle(r, main_deck) for r in raw_battles) if b]
    summary = BattleSummary(battles)

    in_losses: Counter = Counter()
    in_games: Counter = Counter()
    for b in battles:
        in_games.update(set(b.opp_cards))
        if b.result == "win":
            summary.wins += 1
        elif b.result == "draw":
            summary.draws += 1
        else:
            summary.losses += 1
            # A disconnect loss says nothing about the opponent's deck.
            if not b.possible_afk:
                in_losses.update(set(b.opp_cards))
            if b.close:
                summary.close_losses += 1
            if b.opp_crowns == 3 and not b.possible_afk:
                summary.three_crown_losses += 1
            if b.level_gap >= BIG_LEVEL_GAP:
                summary.big_gap_losses.append(b)

    counted_losses = sum(1 for b in battles if b.result == "loss" and not b.possible_afk)
    icons = {name: icon for b in battles for name, icon in b.opp_deck}
    summary.nemeses = [
        Nemesis(card, n, in_games[card], icons.get(card))
        for card, n in in_losses.most_common()
        if n >= 3 and n / counted_losses >= 0.4
    ][:5]
    return summary
