"""Small builders for fake API data so tests don't depend on real players."""

from itertools import count

_clock = count()


def card(name, level=14, max_level=14, elixir=3, evo=0):
    return {"name": name, "level": level, "maxLevel": max_level, "elixirCost": elixir,
            "evolutionLevel": evo, "iconUrls": {}}


def deck(*names, level=14):
    return [card(n, level=level) for n in names]


def battle(my_cards, opp_cards, crowns=(1, 0), type_="PvP", leak=2.0):
    t = next(_clock)
    return {
        "type": type_,
        "battleTime": f"20261028T{t // 3600:02d}{t // 60 % 60:02d}{t % 60:02d}.000Z",
        "team": [{"name": "me", "crowns": crowns[0], "cards": my_cards,
                  "elixirLeaked": leak, "trophyChange": 30 if crowns[0] > crowns[1] else -30}],
        "opponent": [{"name": "them", "crowns": crowns[1], "cards": opp_cards}],
    }
