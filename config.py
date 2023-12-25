#### JSON SETTINGS ####
JSON_INDENT = 2
JSON_SORT_KEYS = False

#### RANDOM SETTINGS ####

# Seed to use for the RNG
# If this is set to None,
# completely random results
# will be generated
RANDOM_SEED = "123456789"  # None

# Random multiplier will be applied
# after calculating all move ratings
# randomly selected between the lower
# range (first value) and higher range
# (second value). If you would like to
# not have any randomness applied, set
# the value to 'None'.
RANDOM_MOVE_MULTIPLIER_RANGE = None  # [0.8,1.2]

#### MOVE RATINGS ####

# Maximum status moves allowed
# This can also be looked at as
# setting the min. number of 
# attacking moves to 'x'.
MAX_STATUS_MOVES = 3

# Maximum attacking moves allowed
# This can also be looked at as
# setting the min. number of
# supporting moves to 'x'.
MAX_ATTACK_MOVES = 4

# Average speed, any
# Pokemon with a speed
# above this prefers
# tailwind/other speed
# boosts, and any Pokemon
# with a speed below it
# prefers trick room /
# speed drops (e.g. curse)
AVERAGE_SPEED = 90

# Moves which benefit slow Pokemon
LOW_SPEED_MOVES = {
    "MOVE_TRICK_ROOM": 6.0,
}

# Moves which benefit fast Pokemon
HIGH_SPEED_MOVES = {
    "MOVE_TAILWIND": 2.0,
}

# Apply doubles boosts, and
# ignores duplicate moves if
# they have different categories
DOUBLES_MODE = True

if DOUBLES_MODE:
    # Doubles status move multiplier
    # i.e. follow me, protect, etc.
    DOUBLES_STATUS_MULTIPLIER = 3.0

    # Doubles spread move multipluer
    # i.e. earthquake, rock slide, etc.
    DOUBLES_MULTIPLIER = 2.0
else:
    # No bonuses for doubles moves
    DOUBLES_STATUS_MULTIPLIER = 0
    DOUBLES_MULTIPLIER = 1.0

# Self-target multiplier
SELF_BOOST_MULTIPLIER = 1.5

# Multi-hit multiplier
MULTI_HIT_MULTIPLIER = 1.0

# Healing move multiplier
HEAL_MULTIPLIER = 1.0

# Boost / nerf for charge/recharge moves
CHARGE_RECHARGE_MULTIPLIER = 0.5

# Multiplier for annoying, hax-based
# moves / effects such as paralysis,
# confusion, attract, etc.
HAX_MULTIPLIER = 1.0

# Multiplier for same-type moves
SAME_TYPE_MULTIPLIER = 3.0

# Multiplier for same-type status moves
SAME_TYPE_STATUS_MULTIPLIER = 1.5

# Crit Stage Multipliers
CRIT_MULTIPLIERS = [
    1,
    1 + 1 / 24,
    1 + 1 / 8,
    1 + 1 / 2,
]

# Type Multipliers
TYPE_MULTIPLIERS = {
    "Fighting": 6 / 4,
    "Ground": 6 / 4,
    "Rock": 6 / 4,
    "Electric": 5 / 4,
    "Ice": 5 / 4,
    "Dragon": 4 / 4,
    "Ghost": 4 / 4,
    "Bug": 4 / 4,
    "Psychic": 4 / 4,
    "Dark": 3 / 4,
    "Steel": 3 / 4,
    "Poison": 2 / 4,
    "Flying": 2 / 4,
    "Water": 2 / 4,
    "Grass": 2 / 4,
    "Fire": 2 / 4,
    "Fairy": 2 / 4,
    "Normal": 1 / 4,
}

# If you want a specific
# move to show up more or
# less, you can put them
# in here - If set to
# zero, the move will
# be skipped
MOVE_MULTIPLIERS = {
    # Signature Moves
    "MOVE_BITTER_BLADE": 6.0,
    "MOVE_ARMOR_CANNON": 6.0,
    "MOVE_GLAIVE_RUSH": 6.0,
    "MOVE_RAGE_FIST": 6.0,
    "MOVE_SALT_CURE": 6.0,
    "MOVE_FIERY_WRATH": 6.0,
    "MOVE_WICKED_BLOW": 6.0,
    "MOVE_SURGING_STRIKES": 6.0,
    # Big Increase
    "MOVE_FAKE_OUT": 12.0,
    "MOVE_FOLLOW_ME": 4.0 * DOUBLES_STATUS_MULTIPLIER, # 12.0
    "MOVE_RAGE_POWDER": 4.0 * DOUBLES_STATUS_MULTIPLIER, # 12.0
    # Fair increase
    "MOVE_PARTING_SHOT": 3.0, 
    "MOVE_VOLT_SWITCH": 3.0, 
    "MOVE_FLIP_TURN": 3.0, 
    "MOVE_U_TURN": 3.0, 
    "MOVE_SPORE": 3.0 * HAX_MULTIPLIER, 
    # Small increase
    "MOVE_ICICLE_CRASH": 1.5,
    "MOVE_THUNDERBOLT": 1.5,
    "MOVE_KNOCK_OFF": 1.5,
    "MOVE_ICE_BEAM": 1.5,
    # Small decrease
    "MOVE_STEEL_BEAM": 0.75,
    "MOVE_LAVA_PLUME": 0.75,
    "MOVE_FOUL_PLAY": 0.75,
    "MOVE_BULLDOZE": 0.75,
    # Fair decrease
    "MOVE_BREAKING_SWIPE": 0.5,
    "MOVE_HELPING_HAND": 0.5,
    "MOVE_TEETER_DANCE": 0.5,
    "MOVE_CIRCLE_THROW": 0.5,
    "MOVE_DRAGON_RUSH": 0.5,
    "MOVE_SKY_ATTACK": 0.5,
    "MOVE_TERA_BLAST": 0.5,
    "MOVE_MAGIC_COAT": 0.5,
    "MOVE_LOW_SWEEP": 0.5,
    "MOVE_BODY_SLAM": 0.5,
    "MOVE_MUD_SHOT": 0.5,
    "MOVE_BLIZZARD": 0.5,
    "MOVE_SCREECH": 0.5,
    "MOVE_SNATCH": 0.5,
    "MOVE_STOMP": 0.5,
    "MOVE_BITE": 0.5,
    # Major decrease
    "MOVE_BABY_DOLL_EYES": 0.25,
    "MOVE_DYNAMIC_PUNCH": 0.25,
    "MOVE_COTTON_SPORE": 0.25,
    "MOVE_FOCUS_PUNCH": 0.25,
    "MOVE_WORRY_SEED": 0.25,
    "MOVE_TORMENT": 0.25,
    "MOVE_MEMENTO": 0.25,
    "MOVE_UPROAR": 0.25,
    "MOVE_FLASH": 0.25,
    "MOVE_SPITE": 0.25,
    "MOVE_GROWL": 0.25,
    "MOVE_LEER": 0.25,
    # Banned completely
    "MOVE_MISTY_EXPLOSION": 0,
    "MOVE_SELF_DESTRUCT": 0,
    "MOVE_VENOM_DRENCH": 0,
    "MOVE_SYNCHRONOISE": 0,
    "MOVE_DREAM_EATER": 0,
    "MOVE_LAST_RESORT": 0,
    "MOVE_SUPERSONIC": 0,
    "MOVE_ACROBATICS": 0,
    "MOVE_TAIL_WHIP": 0,
    "MOVE_EXPLOSION": 0,
    "MOVE_CAPTIVATE": 0,
    "MOVE_SPOTLIGHT": 0, # DOUBLES_STATUS_MULTIPLIER,
    "MOVE_ATTRACT": 0,
    "MOVE_BOUNCE": 0,
    "MOVE_ENDURE": 0, # DOUBLES_STATUS_MULTIPLIER,
    "MOVE_SNORE": 0,
    "MOVE_SOAK": 0,
    "MOVE_PECK": 0,
}

# Rating boosts for status effects
STATUS_MULTIPLIERS = {
    # Hax Statuses
    "par": 1.5 * HAX_MULTIPLIER,
    "slp": 1.5 * HAX_MULTIPLIER,
    "frz": 1.5 * HAX_MULTIPLIER,
    # Other Statuses
    "brn": 1.5,
    "tox": 1.5,
    "psn": 1.2,
}

# Priority stages multiplier
# Has 1 added by default
# e.g. 1 stage is 1.5,
# 2 stages = 2.0, etc.
PRIORITY_MULTIPLIER = 0.5

# Boost multipliers
# Has 1 added by default
# e.g. 1 stage = 1.1
# 2 stages = 1.2, etc.
BOOST_MULTIPLIERS = {
    # Standard
    "atk": 0.1,
    "def": 0.1,
    "spa": 0.1,
    "spd": 0.1,
    "spe": 0.1,
    # Special
    "accuracy": 0.1 * HAX_MULTIPLIER,
    "evasion": 0.1 * HAX_MULTIPLIER,
}

FLAG_MULTIPLIERS = {
    # Positive Flags
    "bypasssub": 1.3,
    "defrost": 1.3,
    "heal": 1.0 * HEAL_MULTIPLIER,
    # Negative Flags
    "cantusetwice": 1.0,  # Gigaton hammer is based
    "futuremove": 0.5,
    "recharge": 1.0 * CHARGE_RECHARGE_MULTIPLIER,
    "charge": 1.0 * CHARGE_RECHARGE_MULTIPLIER,
    # Identifying Flags
    "slicing": 1.0,
    "bullet": 1.0,
    "punch": 1.0,
    "sound": 1.0,
    "pulse": 1.0,
    "dance": 1.0,
    "wind": 1.0,
    "bite": 1.0,
    # Effect Flags
    "reflectable": 1.0,
    "distance": 1.0,
    "protect": 1.0,
    "contact": 1.0,
    "gravity": 1.0,
    "powder": 1.0,
    "mirror": 1.0,
    "snatch": 1.0,
    # Fail Flags
    "failinstruct": 1.0,
    "failcopycat": 1.0,
    "failmefirst": 1.0,
    "failencore": 1.0,
    "failmimic": 1.0,
    "noparentalbond": 1.0,
    "nosleeptalk": 1.0,
    "noassist": 1.0,
    "nonsky": 1.0,
    # Other Flags
    "mustpressure": 1.0,
    "pledgecombo": 1.0,
    "allyanim": 1.0,
}

# Volatile Status multipliers
# When applied to self, modifiers
# will be used as-is (if negative)
# When applied to others, modifiers
# will be converted to even value
VOLATILE_STATUS_MULTIPLIERS = {
    # General Effects
    "syrupbomb": 1.5,
    "saltcure": 1.5,
    "partiallytrapped": 1.3,
    "destinybond": 1.3,
    "substitute": 1.3,
    "healblock": 1.3,
    "smackdown": 1.3,
    "leechseed": 1.3,
    "confusion": 1.3 * HAX_MULTIPLIER,
    "minimize": 1.3 * HAX_MULTIPLIER,
    "octolock": 1.3,
    "flinch": 1.3 * HAX_MULTIPLIER,
    "yawn": 1.3 * HAX_MULTIPLIER,
    "sparklingaria": 1.2,
    "dragoncheer": 1.2,
    "focusenergy": 1.2,
    "telekinesis": 1.2,
    "magnetrise": 1.2,
    "stockpile": 1.2,
    "magiccoat": 1.2,
    "embargo": 1.2,
    "snatch": 1.2,
    "powder": 1.2,
    "grudge": 1.2,
    "defensecurl": 1.1,
    "miracleeye": 1.1,
    "gastroacid": 1.1,
    "powershift": 1.1,
    "powertrick": 1.1,
    "laserfocus": 1.1,
    "foresight": 1.1,
    "electrify": 1.1,
    "nightmare": 1.1,
    "aquaring": 1.1,
    "imprison": 1.1,
    "disable": 1.1,
    "attract": 1.1 * HAX_MULTIPLIER,
    "torment": 1.1,
    "charge": 1.1,
    "encore": 1.1,
    "taunt": 1.1,
    "tarshot": 1.0,
    "endure": 1.0,
    "uproar": 1.0,
    # Doubles Effecs
    "burningbulwark": 1.5 * DOUBLES_STATUS_MULTIPLIER,
    "banefulbunker": 1.5 * DOUBLES_STATUS_MULTIPLIER,
    "kingsshield": 1.5 * DOUBLES_STATUS_MULTIPLIER,
    "spikyshield": 1.5 * DOUBLES_STATUS_MULTIPLIER,
    "silktrap": 1.5 * DOUBLES_STATUS_MULTIPLIER,
    "obstruct": 1.5 * DOUBLES_STATUS_MULTIPLIER,
    "protect": 1.5 * DOUBLES_STATUS_MULTIPLIER,
    "ragepowder": 1.5 * DOUBLES_STATUS_MULTIPLIER,
    "followme": 1.5 * DOUBLES_STATUS_MULTIPLIER,
    "spotlight": 1.0 * DOUBLES_STATUS_MULTIPLIER,
    # Negative Self-Effects
    "glaiverush": 1.0,
    "noretreat": 1.0,
    "roost": 1.0,
    "mustrecharge": 1.0,  # Handled by flags
    "lockedmove": 0.5,
}

# Maximum number of same-type moves
# If set to none, no maximum is enforced
MAX_SAME_TYPE_MOVES = 2

#### STAT CALCULATIONS ####

# Multiply hp stat by this
# in calculations to account
# for it generally being lower
# than other base stats
HP_MULTIPLIER = 1.5

# Above this is offensive-focused
# below this is defensive-focused
OFFDEF_RATIO_CUTOFF = 1.2

# Pokemon more than this are physically orientated
ATK_RATIO_CUTOFF = 1.1

# Pokemon between this are mixed

# Pokemon less than this are specially orientated
SPA_RATIO_CUTOFF = 0.9

# If the pokemon's offensive type
# is outside of the cutoff range,
# apply this multiplier instead
# of using the ratio multiplier
RATIO_CUTOFF_MULTIPLIER = 0.5

#### GENERAL SETTINGS ###

# Output folder
OUT_FOLDER = "output"

# Output filename
OUT_FILENAME = "battle_frontier_sets.json"

# Default file, if no arguments provided
DEFAULT_FILE = "input/teachable_learnsets.h"
