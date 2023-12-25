SELF_TARGET = ["self", "allySide", "allyTeam"]

SINGLE_TARGET = ["normal", "randomNormal", "adjacentFoe"]

MULTI_TARGET = ["allAdjacentFoes", "allAdjacent"]

OTHER_TARGET = SINGLE_TARGET + MULTI_TARGET

# Protect moves
# For preventing duplicates
STATUS_PROTECT = [
    "burningbulwark",
    "banefulbunker",
    "kingsshield",
    "spikyshield",
    "silktrap",
    "obstruct",
    "protect",
    "endure",
]

# Redirect moves
# For preventing duplicates
STATUS_REDIRECT = [
    "ragepowder",
    "spotlight",
    "followme",
]

# Special Cases
SPECIAL_CASES = {
    "meowsticfemale": "meowsticf",
    "indeedeefemale": "indeedeef",
    "calyrexicerider": "calyrexice",
    "calyrexshadowrider": "calyrexshadow",
    "deoxysnormal": "deoxys",
    "mimejr": "mime jr.",
    "basculinredstriped": "basculin",
    "flabebe": "flabebe-red-flower",
    "floette": "floette-red-flower",
    "florges": "florges-red-flower",
    "zygarde": "zygarde-complete",
    "typenull": "type: null",
    "jangmoo": "jangmo-o",
    "sirfetchd": "sirfetch'd",
    "mrrime": "mr. rime",
    "wormadamsandycloak": "wormadamsandy",
    "wormadamtrashcloak": "wormadamtrash",
    "floetteeternalflower": "floetteeternal",
    "urshifurapidstrikestyle": "urshifurapidstrike",
    "paldeantauroscombatbreed": "taurospaldeacombat",
    "paldeantaurosblazebreed": "taurospaldeablaze",
    "paldeantaurosaquabreed": "taurospaldeaaqua",
    "paldeanwooper": "wooperpaldea",
    "palafinzeroform": "palafin",
    "gimmighoulchestform": "gimmighoul",
    "mrmime-galar": "mr. mime-galar",
    "farfetchd-galar": "farfetch'd-galar",
}

NATURES = {
    "adamant": {"inc": "atk", "dec": "spa"},
    "bashful": {"inc": None, "dec": None},
    "bold": {"inc": "def", "dec": "atk"},
    "brave": {"inc": "atk", "dec": "spe"},
    "calm": {"inc": "spd", "dec": "atk"},
    "careful": {"inc": "spd", "dec": "spa"},
    "docile": {"inc": None, "dec": None},
    "gentle": {"inc": "spd", "dec": "def"},
    "hardy": {"inc": None, "dec": None},
    "hasty": {"inc": "spe", "dec": "def"},
    "impish": {"inc": "def", "dec": "spa"},
    "jolly": {"inc": "spe", "dec": "spa"},
    "lax": {"inc": "def", "dec": "spd"},
    "lonely": {"inc": "atk", "dec": "def"},
    "mild": {"inc": "spa", "dec": "def"},
    "modest": {"inc": "spa", "dec": "atk"},
    "naive": {"inc": "spe", "dec": "spd"},
    "naughty": {"inc": "atk", "dec": "spd"},
    "quiet": {"inc": "spa", "dec": "spe"},
    "quirky": {"inc": None, "dec": None},
    "rash": {"inc": "spa", "dec": "spd"},
    "relaxed": {"inc": "def", "dec": "spe"},
    "sassy": {"inc": "spd", "dec": "spe"},
    "serious": {"inc": None, "dec": None},
    "timid": {"inc": "spe", "dec": "atk"},
}

NATURE_MODIFIERS = {
    "adamant": {"atk": 1.1, "def": 1.0, "spa": 0.9, "spd": 1.0, "spe": 1.0},
    "bashful": {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 1.0, "spe": 1.0},
    "bold": {"atk": 1.0, "def": 1.1, "spa": 1.0, "spd": 1.0, "spe": 1.0},
    "brave": {"atk": 1.1, "def": 1.0, "spa": 1.0, "spd": 1.0, "spe": 0.9},
    "calm": {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 1.1, "spe": 1.0},
    "careful": {"atk": 1.0, "def": 1.0, "spa": 0.9, "spd": 1.1, "spe": 1.0},
    "docile": {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 1.0, "spe": 1.0},
    "gentle": {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 1.1, "spe": 0.9},
    "hardy": {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 1.0, "spe": 1.0},
    "hasty": {"atk": 1.0, "def": 0.9, "spa": 1.0, "spd": 1.0, "spe": 1.1},
    "impish": {"atk": 1.1, "def": 1.0, "spa": 1.0, "spd": 0.9, "spe": 1.0},
    "jolly": {"atk": 1.0, "def": 1.0, "spa": 0.9, "spd": 1.0, "spe": 1.1},
    "lax": {"atk": 1.1, "def": 0.9, "spa": 1.0, "spd": 1.0, "spe": 1.0},
    "lonely": {"atk": 1.1, "def": 0.9, "spa": 1.0, "spd": 1.0, "spe": 1.0},
    "mild": {"atk": 1.0, "def": 0.9, "spa": 1.1, "spd": 1.0, "spe": 1.0},
    "modest": {"atk": 1.0, "def": 0.9, "spa": 1.1, "spd": 1.0, "spe": 1.0},
    "naive": {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 0.9, "spe": 1.1},
    "naughty": {"atk": 1.1, "def": 1.0, "spa": 1.0, "spd": 0.9, "spe": 1.0},
    "quiet": {"atk": 1.0, "def": 1.0, "spa": 1.1, "spd": 1.0, "spe": 0.9},
    "quirky": {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 1.0, "spe": 1.0},
    "rash": {"atk": 1.0, "def": 1.0, "spa": 1.1, "spd": 0.9, "spe": 1.0},
    "relaxed": {"atk": 1.0, "def": 1.1, "spa": 1.0, "spd": 1.0, "spe": 0.9},
    "sassy": {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 1.1, "spe": 0.9},
    "serious": {"atk": 1.0, "def": 1.0, "spa": 1.0, "spd": 1.0, "spe": 1.0},
    "timid": {"atk": 1.0, "def": 0.9, "spa": 1.0, "spd": 1.0, "spe": 1.1},
}
