import pytest

from app.analysis.battles import summarize
from app.analysis.coach import coach
from app.analysis.deck import analyze_deck
from app.analysis.levels import display_level
from app.cr_client import InvalidTag, normalize_tag

from .helpers import battle, card, deck

GOOD_DECK = ["Hog Rider", "Musketeer", "Valkyrie", "Fireball", "The Log", "Cannon", "Ice Spirit", "Skeletons"]
BAIT = ["Goblin Barrel", "The Log", "Princess", "Goblin Gang", "Knight", "Inferno Tower", "Rocket", "Ice Spirit"]


def titles(tips):
    return [t.title for t in tips]


@pytest.mark.parametrize("raw", ["#PV20Q9QQ8", "pv20q9qq8", "  #pv2oq9qq8 "])
def test_normalize_tag(raw):
    assert normalize_tag(raw) == "#PV20Q9QQ8"


@pytest.mark.parametrize("raw", ["", "#AB", "hello world", "#PV20Q9QQ8XXXXX"])
def test_normalize_tag_rejects_garbage(raw):
    with pytest.raises(InvalidTag):
        normalize_tag(raw)


def test_display_level_uses_one_scale_for_all_rarities():
    assert display_level(card("Knight", level=16, max_level=16)) == 16
    assert display_level(card("Battle Ram", level=14, max_level=14)) == 16
    assert display_level(card("Bandit", level=7, max_level=8)) == 15


def test_balanced_deck_has_every_role():
    report = analyze_deck(deck(*GOOD_DECK))
    assert report.missing_roles == []


def test_deck_without_air_or_spells_is_flagged():
    report = analyze_deck(deck("Giant", "Knight", "Valkyrie", "Prince", "Barbarians", "Mini P.E.K.K.A", "Skeletons", "Bomber"))
    missing = {r.key for r in report.missing_roles}
    assert {"air_defense", "small_spell", "big_spell"} <= missing
    tips = coach(report, summarize([], set()))
    assert tips[0].severity == 3
    assert "You're weak against air troops" in titles(tips)


def test_upgrade_priority_orders_by_gap():
    cards = deck(*GOOD_DECK[:6]) + [card("Ice Spirit", level=11), card("Skeletons", level=13)]
    report = analyze_deck(cards)
    assert [(c.name, gap) for c, gap in report.upgrade_priority] == [("Ice Spirit", 3), ("Skeletons", 1)]
    assert "Upgrade Ice Spirit first" in titles(coach(report, summarize([], set())))


def test_summary_counts_and_nemesis():
    mine = deck(*GOOD_DECK)
    raw = [battle(mine, deck(*BAIT), crowns=(0, 1)) for _ in range(4)]
    raw += [battle(mine, deck(*GOOD_DECK), crowns=(3, 0)) for _ in range(3)]
    raw.append(battle(mine, deck(*GOOD_DECK), type_="friendly", crowns=(0, 3)))

    s = summarize(raw, set(GOOD_DECK))
    assert (s.games, s.wins, s.losses, s.close_losses) == (7, 3, 4, 4)
    assert s.nemeses[0].card in BAIT and s.nemeses[0].losses_with == 4
    assert "Most of your losses are close" in titles(coach(analyze_deck(mine), s))


def test_disconnects_are_labeled_not_blamed_on_opponent():
    mine = deck(*GOOD_DECK)
    raw = [battle(mine, deck(*BAIT), crowns=(0, 3), leak=20) for _ in range(3)]
    s = summarize(raw, set(GOOD_DECK))
    assert all(b.possible_afk for b in s.battles)
    assert s.nemeses == []


def test_outleveled_losses_with_other_deck():
    weak = deck(*BAIT, level=12)
    raw = [battle(weak, deck(*GOOD_DECK, level=14), crowns=(0, 2)) for _ in range(3)]
    s = summarize(raw, set(GOOD_DECK))
    tips = coach(analyze_deck(deck(*GOOD_DECK)), s)
    tip = next(t for t in tips if "lower card levels" in t.title)
    assert "different deck" in tip.why
