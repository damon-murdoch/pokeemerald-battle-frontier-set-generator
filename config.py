#### JSON SETTINGS ####
JSON_INDENT = 2
JSON_SORT_KEYS = False

#### RANDOM SETTINGS ####

# Seed to use for the RNG
# If this is set to None, 
# completely random results
# will be generated
RANDOM_SEED = '123456789' # None

# Random multiplier will be applied 
# after calculating all move ratings
# randomly selected between the lower
# range (first value) and higher range
# (second value). If you would like to
# not have any randomness applied, set
# the value to 'None'. 
RANDOM_MOVE_MULTIPLIER_RANGE = None # [0.8,1.2]

#### MOVE RATINGS ####

# Multiply spread moves by this amount
SPREAD_MULTIPLIER = 1.5

# Multiply healing move 
HEAL_MULTIPLIER = 1.0

# Multiplier for same-type moves
SAME_TYPE_MULTIPLIER = 1.5

# Multiplier for same-type status moves
SAME_TYPE_STATUS_MULTIPLIER = 1.3

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

#### GENERAL SETTINGS ###

# Output folder
OUT_FOLDER = "output"

# Output filename
OUT_FILENAME = "battle_frontier_sets.json"

# Default file, if no arguments provided
DEFAULT_FILE = "input/teachable_learnsets.h"
