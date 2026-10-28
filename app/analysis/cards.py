"""Hand-written card knowledge the API does not give us: what job each card does.

Cards missing from these sets simply don't count toward a role. Add new cards
here when Supercell releases them.
"""

WIN_CONDITIONS = {
    "Hog Rider", "Royal Giant", "Giant", "Golem", "Lava Hound", "Balloon", "X-Bow",
    "Mortar", "Graveyard", "Goblin Barrel", "Miner", "Ram Rider", "Battle Ram",
    "Royal Hogs", "Elixir Golem", "Goblin Giant", "Electro Giant", "Wall Breakers",
    "Three Musketeers", "Skeleton Barrel", "Goblin Drill", "Sparky", "Bandit",
    "Royal Recruits", "Giant Skeleton", "Rocket",
}

AIR_DEFENSE = {
    "Musketeer", "Archers", "Minions", "Minion Horde", "Baby Dragon", "Electro Wizard",
    "Wizard", "Ice Wizard", "Mega Minion", "Bats", "Flying Machine", "Inferno Dragon",
    "Inferno Tower", "Tesla", "Archer Queen", "Hunter", "Executioner", "Firecracker",
    "Dart Goblin", "Princess", "Magic Archer", "Spear Goblins", "Electro Dragon",
    "Phoenix", "Witch", "Mother Witch", "Electro Spirit", "Ice Spirit", "Fire Spirit",
    "Zappies", "Little Prince", "Skeleton Dragons", "Three Musketeers", "X-Bow",
    "Goblin Hut", "Furnace", "Rascals",
}

SPLASH = {
    "Baby Dragon", "Wizard", "Executioner", "Bowler", "Valkyrie", "Dark Prince",
    "Electro Wizard", "Bomber", "Ice Wizard", "Witch", "Mega Knight", "Princess",
    "Firecracker", "Magic Archer", "Electro Dragon", "Bomb Tower", "Skeleton Dragons",
    "Fire Spirit", "Electro Spirit", "Sparky", "Mortar", "Phoenix", "Furnace",
    "Royal Ghost", "Skeleton King", "Electro Giant", "Hunter", "Giant Skeleton",
}

SMALL_SPELLS = {
    "Zap", "The Log", "Arrows", "Giant Snowball", "Barbarian Barrel", "Tornado",
    "Royal Delivery", "Earthquake", "Goblin Curse",
}

BIG_SPELLS = {"Fireball", "Poison", "Rocket", "Lightning", "Void"}

BUILDINGS = {
    "Cannon", "Tesla", "Inferno Tower", "Bomb Tower", "Goblin Cage", "Tombstone",
    "Furnace", "Goblin Hut", "Barbarian Hut", "X-Bow", "Mortar", "Goblin Drill",
}

TANK_KILLERS = {
    "P.E.K.K.A", "Mini P.E.K.K.A", "Inferno Tower", "Inferno Dragon", "Hunter",
    "Barbarians", "Elite Barbarians", "Mighty Miner", "Lumberjack", "Sparky",
    "Goblin Cage", "Cannon", "Minion Horde", "Prince",
}

# Beginner-friendly advice for cards that often beat new players.
COUNTER_TIPS = {
    "Goblin Barrel": "Keep a small spell (The Log, Zap, Arrows) ready and drop it on the goblins as they land next to your tower.",
    "The Log": "The Log is often part of a 'bait' deck. Avoid playing all your small ground troops (goblins, skeletons) at the same time.",
    "Hog Rider": "Place a building or a tank killer (Cannon, Tesla, Mini P.E.K.K.A) in the middle of your side so the Hog turns away from the tower.",
    "Balloon": "Keep two cards that hit air. Kill the Balloon before it reaches your tower; Musketeer or Minions work well.",
    "Lava Hound": "You need strong air defense. Kill the Hound near the bridge, then splash the pups with Wizard, Baby Dragon or Arrows.",
    "Golem": "Golem players spend 8 elixir at the back. Punish them by attacking the other lane right away.",
    "Mega Knight": "Don't put troops in a group where it jumps. Use a tank killer like Mini P.E.K.K.A or Inferno, or distract it with cheap troops.",
    "P.E.K.K.A": "Swarm it with cheap troops like Skeletons or Goblin Gang, or pull it to the middle with a building.",
    "Graveyard": "Play a splash troop (Valkyrie, Wizard) on top of the skeletons, or use Poison on them.",
    "X-Bow": "Attack the X-Bow before it locks onto your tower, or send a tank to soak the shots.",
    "Royal Giant": "Use a tank killer (Inferno, Mini P.E.K.K.A, Hunter) as soon as it crosses the bridge.",
    "Miner": "Keep a cheap troop ready to place on the Miner when it pops up next to your tower.",
    "Sparky": "Reset Sparky with Zap, Electro Wizard or Electro Spirit, or kill it with a swarm.",
    "Goblin Gang": "Answer it with a cheap splash card or small spell (Zap, The Log, Arrows, Valkyrie) instead of single-target troops.",
    "Witch":"Use a spell or a splash troop to clear the skeletons, then kill the Witch fast.",
    "Princess": "Use The Log, Arrows or a fast troop to take her out across the river.",
    "Inferno Tower": "Reset it with Zap or Electro Wizard, or bring two win conditions at once.",
    "Electro Giant": "Avoid placing many small troops near it; use a building to pull it, and buildings or spells for support troops.",
    "Elite Barbarians": "Swarm them with Skeletons or Goblin Gang, or use a building to pull them.",
    "Three Musketeers": "Use Fireball or Lightning when they're grouped, or attack the other lane when they're split.",
}

ROLE_SETS = {
    "win_condition": WIN_CONDITIONS,
    "air_defense": AIR_DEFENSE,
    "splash": SPLASH,
    "small_spell": SMALL_SPELLS,
    "big_spell": BIG_SPELLS,
    "tank_answer": BUILDINGS | TANK_KILLERS,
}
