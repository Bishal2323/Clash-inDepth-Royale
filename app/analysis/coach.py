"""Coaching rules: each rule looks at the analysis and may return one tip.

To add a tip, write a function decorated with @rule that returns a Tip or None.
Tips are sorted by severity; the top three become "Fix these first".
Elixir leaked is deliberately not used here: waiting can be the right play, and
the API can't tell us when or why elixir was lost.
"""

from dataclasses import dataclass

from .battles import BattleSummary
from .cards import COUNTER_TIPS
from .deck import HEAVY_DECK, LIGHT_DECK, DeckReport

HIGH, MEDIUM, LOW = 3, 2, 1


@dataclass
class Tip:
    severity: int
    title: str
    why: str
    action: str

    @property
    def severity_label(self) -> str:
        return {HIGH: "high", MEDIUM: "medium", LOW: "low"}[self.severity]


RULES = []


def rule(fn):
    RULES.append(fn)
    return fn


def coach(deck: DeckReport, summary: BattleSummary) -> list[Tip]:
    tips = [tip for r in RULES if (tip := r(deck, summary))]
    return sorted(tips, key=lambda t: -t.severity)


# --- Deck rules ---------------------------------------------------------------

@rule
def no_win_condition(deck, summary):
    if deck.role("win_condition").ok:
        return None
    return Tip(HIGH, "Your deck has no win condition",
               "Without a card built to hit towers, it's hard to get crowns even when you defend well.",
               "Add one win condition, like Hog Rider, Giant or Goblin Barrel, and build the deck around it.")


@rule
def weak_air_defense(deck, summary):
    air = deck.role("air_defense").cards
    if len(air) >= 2:
        return None
    have = f"Only {air[0]} can hit air." if air else "No card in your deck can hit air."
    return Tip(HIGH if not air else MEDIUM, "You're weak against air troops",
               f"{have} Balloon, Lava Hound and Minions will be hard to stop.",
               "Make sure at least two cards hit air, like Musketeer, Archers, Minions or Baby Dragon.")


@rule
def no_small_spell(deck, summary):
    if deck.role("small_spell").ok:
        return None
    return Tip(MEDIUM, "Add a small spell",
               "Swarms like Goblin Gang, Skeleton Army or Goblin Barrel will be hard to answer.",
               "Swap a card for Zap, The Log, Arrows or Giant Snowball.")


@rule
def no_splash(deck, summary):
    if deck.role("splash").ok:
        return None
    return Tip(MEDIUM, "No splash damage",
               "Groups of troops (Skeleton Army, Minion Horde, Barbarians) will overwhelm single-target cards.",
               "Add a splash troop like Valkyrie, Baby Dragon, Wizard or Bowler.")


@rule
def no_tank_answer(deck, summary):
    if deck.role("tank_answer").ok:
        return None
    return Tip(MEDIUM, "Nothing stops big tanks",
               "Giants, Golems and P.E.K.K.As will walk to your tower.",
               "Add a tank killer (Mini P.E.K.K.A, Inferno Tower, Hunter) or a building (Cannon, Tesla).")


@rule
def no_big_spell(deck, summary):
    if deck.role("big_spell").ok:
        return None
    return Tip(LOW, "Consider a bigger spell",
               "A big spell kills medium troops like Musketeer or Wizard and can finish a tower.",
               "Fireball and Poison are good first choices.")


@rule
def deck_cost(deck, summary):
    if deck.avg_elixir > HEAVY_DECK:
        return Tip(MEDIUM, f"Your deck is expensive ({deck.avg_elixir} elixir on average)",
                   "With many heavy cards you'll often have nothing to play when the opponent attacks.",
                   "Swap one or two expensive cards for cheap ones (1–3 elixir) to keep up.")
    if deck.avg_elixir and deck.avg_elixir < LIGHT_DECK:
        return Tip(LOW, f"Your deck is very cheap ({deck.avg_elixir} elixir on average)",
                   "Cheap decks are fast but can struggle to stop big pushes.",
                   "Make sure you still have a strong defender for tanks.")
    return None


@rule
def underleveled_cards(deck, summary):
    if not deck.upgrade_priority:
        return None
    card, gap = deck.upgrade_priority[0]
    others = [c.name for c, _ in deck.upgrade_priority[1:3]]
    also = f" Then: {', '.join(others)}." if others else ""
    return Tip(HIGH if gap >= 2 else LOW, f"Upgrade {card.name} first",
               f"{card.name} is {gap} level{'s' if gap > 1 else ''} behind your best cards, so it loses trades it should win.",
               f"Spend your gold on {card.name} before cards outside this deck.{also}")


# --- Battle rules -------------------------------------------------------------

@rule
def outleveled_losses(deck, summary):
    losses = summary.big_gap_losses
    if len(losses) < 2:
        return None
    gap = sum(b.level_gap for b in losses) / len(losses)
    other_deck = sum(1 for b in losses if not b.used_main_deck)
    hint = (" Most of them were with a different deck than your main one."
            if other_deck > len(losses) / 2 else "")
    return Tip(HIGH, f"{len(losses)} losses came with much lower card levels",
               f"In those games your cards were about {gap:.1f} levels below your opponent's.{hint}",
               "Play your best-leveled deck in Ladder and Ranked. Test new decks in friendlies or events.")


@rule
def nemesis_card(deck, summary):
    if not summary.nemeses:
        return None
    n = summary.nemeses[0]
    counted = summary.losses - sum(1 for b in summary.battles if b.possible_afk)
    advice = COUNTER_TIPS.get(n.card, f"Watch for {n.card} and save a card that answers it.")
    return Tip(MEDIUM, f"{n.card} keeps beating you",
               f"{n.card} was in {n.losses_with} of your {counted} losses.",
               advice)


@rule
def three_crowned(deck, summary):
    if summary.three_crown_losses < 3 or summary.three_crown_losses / max(summary.losses, 1) < 0.3:
        return None
    return Tip(MEDIUM, "You often lose all three towers",
               f"{summary.three_crown_losses} of your {summary.losses} losses were 3-crown losses.",
               "When you lose a tower, switch to defense. Defend, then counterattack with what survives.")


@rule
def close_losses(deck, summary):
    if summary.losses < 4 or summary.close_losses / summary.losses < 0.5:
        return None
    return Tip(LOW, "Most of your losses are close",
               f"{summary.close_losses} of your {summary.losses} losses were by one crown, so you're near winning those.",
               "In double elixir, defend first and attack with the survivors instead of sending your win condition alone.")
