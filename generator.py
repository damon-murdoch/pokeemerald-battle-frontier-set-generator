# Global Imports
import json as JSON
import requests
import sys, os
import random
import re

# Above this is offensive-focused
# below this is defensive-focused
RATIO_CUTOFF = 1.2

# Data File
import src.data as DATA

def get_bst(base_stats):
    return (
        base_stats["hp"]
        + base_stats["atk"]
        + base_stats["def"]
        + base_stats["spa"]
        + base_stats["spd"]
        + base_stats["spe"]
    )


def get_atk_spa_ratio(base_stats, nature='quirky'):
    # Get atk/spa ratio (atk > 1, spa < 1)
    return (base_stats["atk"] * DATA.NATURE_MODIFIERS[nature]['atk']) / (base_stats["spa"] * DATA.NATURE_MODIFIERS[nature]['spa'])


def get_offensive_defensive_ratio(base_stats, nature='quirky'):
    # Calculates roughly if the Pokemon is more offensive or defensive orientated, by comparing the average of the
    # defensive stats when compared to the highest of the Pokemon's special attack and regular attack stats.
    return max(
        base_stats["spa"] * DATA.NATURE_MODIFIERS[nature]['spa'], 
        base_stats["atk"] * DATA.NATURE_MODIFIERS[nature]['atk']
    ) / (
        (base_stats["hp"] + (
            base_stats["def"] * DATA.NATURE_MODIFIERS[nature]['def']
        ) + (
            base_stats["spd"] * DATA.NATURE_MODIFIERS[nature]['spd']
        )) / 3
    )


def parse_moves(moves_list):
    # List of moves
    moves = []

    # Loop over all of the moves
    for move in moves_list:
        # Convert the move name to showdown format
        name = convert_to_showdown_format(move[4:])

        # Move found
        if name in MOVES:
            # Add move to list
            moves.append(MOVES[name])
        # Move not found
        if name not in MOVES:
            print(f"Move not found: {name}")

    # Return moves list
    return moves

def get_nature(inc, dec):

    # Loop over all of the natures
    for nature in DATA.NATURES:
        data = DATA.NATURES[nature]
        if data['inc'] == inc and data['dec'] == dec:
            return nature

    print(f"No nature found for stats {inc}, {dec} - Returning neutral nature")

    # No matching nature
    # Return random neutral nature
    return random.choice([
        'bashful', 'docile', 'hardy', 'quirky', 'serious'
    ])

def get_best_nature(base_stats):

    # Best stat (non-hp)
    best_nature_stat = None
    best_nature_stat_value = None

    # Worst offensive stat
    worst_offensive_stat = None
    worst_offensive_stat_value = None

    # Loop over the base stats
    for stat in base_stats:

        # Skip hp stat, no natures
        if stat == 'hp': continue

        # Best stat value not assigned yet, or current stat is better
        if best_nature_stat_value == None or base_stats[stat] > best_nature_stat_value:
            # Update best stat
            best_nature_stat_value = base_stats[stat]
            best_nature_stat = stat

        # Get worst offensive stat
        if stat in ['atk', 'spa', 'spe']: 

            # Worst offensive stat value not assigned yet, or current offensive stat is worse
            if worst_offensive_stat_value == None or base_stats[stat] < worst_offensive_stat_value:

                # Update worst offensive stat
                worst_offensive_stat_value = base_stats[stat]
                worst_offensive_stat = stat

    # Get the best nature for the given spread
    return get_nature(best_nature_stat, worst_offensive_stat)

def get_best_moves(moves, species, nature):

    # Move ratings array
    move_ratings = []

    # Get the base stats for the species
    base_stats = species["baseStats"]

    # Get the offensive (atk/spa) ratio
    off_ratio = get_atk_spa_ratio(base_stats)

    # Get the offensive/defensive ratio for the species
    offdef_ratio = get_offensive_defensive_ratio(base_stats)

    print(
        f"Offensive/Defensive ratio: {round(offdef_ratio,2)}, off. ratio: {round(off_ratio,2)} ..."
    )

    # Loop over the moves
    for move in moves:

        # Base Rating
        rating = 1

        # Multiply rating by the accuracy
        rating *= move["accuracy"] / 100

        # Move has flags
        if "flags" in move:
            # Iterate over the flags
            for flag in move["flags"]:
                # If the flag has a boost
                if flag in DATA.FLAG_BOOSTS:
                    # Apply the rating boost
                    rating *= DATA.FLAG_BOOSTS[flag]

        # Move heals the user
        if "heal" in move:
            heal = move["heal"]
            rating *= 1.0 + (heal[0]/heal[1])

        # Move drains the target
        if "drain" in move:
            drain = move["drain"]
            rating *= 1.0 + (drain[0]/drain[1])

        # Move has boosts
        if "boosts" in move:
            # Loop over the stats
            for stat in move["boosts"]:
                # Add ~10% for 1x boost (~20% for 2x boost), etc.
                rating *= 1.0 + (abs(move["boosts"][stat]) / 10)

        # Move has self-effects
        if "self" in move:
            self = move["self"]

            # Move has self-boosts
            if "boosts" in self:
                # Loop over the stats
                for stat in self["boosts"]:
                    # Dereference boost value
                    boost = self["boosts"][stat]

                    # Add/Sub ~10% for 1x boost (~20% for 2x boost), etc.
                    rating *= 1.0 + (boost / 10)

            # Move has self-volatile status
            if "volatileStatus" in self:
                # Reduce rating 
                rating /= 1.5

        # Move has a secondary effect, and is not none
        if "secondary" in move and move["secondary"] != None:
            secondary = move["secondary"]

            # Chance is defined
            if "chance" in secondary:

                # Base boost value
                boost = 100

                # Secondary status defined
                if "status" in secondary:
                    # Get the boost defined for the status
                    boost = DATA.STATUS_BOOSTS[secondary["status"]]

                # Secondary boosts defined
                if "boosts" in secondary:
                    for stat in secondary["boosts"]:
                        # Add ~10% for 1x boost (~20% for 2x boost), etc.
                        boost *= 1.0 + (abs(secondary["boosts"][stat]) / 10)

                # Volatile status defined
                if "volatileStatus" in secondary:
                    boost *= 1.5 # 1.5x for volatile status

                # Adds up to ~2x per effect chance
                rating *= 1.0 + ((secondary["chance"] / 100) * (boost / 100))

        # If the move has a status
        if "status" in move:
            # Multiply the rating based on the status
            rating *= DATA.STATUS_BOOSTS[move["status"]]

        # Move category is status
        if move["category"] == "Status":

            # Move is one of the primary types
            if move["type"] in species["types"]:
                rating *= 1.2 # Increase selection odds

            # Divide by offdef ratio
            rating /= offdef_ratio

        else: # Move is offensive

            # Move is one of the primary types
            if move["type"] in species["types"]:
                rating *= 1.5 # Apply STAB boost to rating

            # If physical, multiply by ratio
            if move["category"] == "Physical":
                rating *= off_ratio

            # If special, divide by ratio
            if move["category"] == "Special":
                rating /= off_ratio

            # Multiply rating by base power
            rating *= move["basePower"] / 100

        # Add the move rating to the list
        move_ratings.append({"name": move["name"], "category": move["category"], "type": move["type"], "rating": rating})

    # Sort the ratings from low to high
    move_ratings.sort(key=lambda x: x["rating"], reverse=True)

    # Best moves list
    best_moves = []

    # Loop over the rated moves
    for move in move_ratings:

        # Assume best move
        best = True

        # Loop over the best moves
        for best_move in best_moves:
            if move["category"] == best_move["category"] and move["type"] == best_move["type"]:
                best = False # Worse move with same type/category

        # Best is still set
        if best == True:
            # Add to best moves list
            best_moves.append(move)

    # Return best moves
    return best_moves

def get_best_evs(moves, base_stats, nature):

    # Eligible stats for investing in
    eligible_stats = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']

    # Remove whichever stat is reduced by the nature
    eligible_stats.remove(DATA.NATURES[nature]['dec'])

    # Number of phys/spec moves
    moves_physical = 0
    moves_special = 0

    # Loop over the moves
    for move in moves:
        # If move is physical, increment physical counter
        if move["category"] == "Physical": moves_physical += 1
        # If move is special, implement special counter
        elif move["category"] == "Special": moves_special += 1

    # If there are no physical attacks, and atk is still eligible
    if moves_physical == 0 and 'atk' in eligible_stats:
        eligible_stats.remove('atk') # Remove it, no need

    # If there are no special attacks, and spa is still eligible
    if moves_special == 0 and 'spa' in eligible_stats:
        eligible_stats.remove('spa') # Remove it, no need

    # While more than two eligible stats
    while(len(eligible_stats) > 2):
        
        # Record worst stats
        worst_stat = None
        worst_stat_value = None

        # Loop over eligible stats
        for stat in eligible_stats:

            # Get the value from the stat
            value = base_stats[stat]

            # Stat is hp
            if stat == 'hp':
                # Multiply by 1.5x
                value *= 1.5

            else: # Any other stat
                # Apply nature modifiers to the stat
                value *= DATA.NATURE_MODIFIERS[nature][stat]

            # If the worst stat is unset, or current stat is worse
            if worst_stat_value == None or worst_stat_value > value:
                # Update worst stat, worst stat value
                worst_stat_value = value
                worst_stat = stat
        
        # Remove the worst stat from the list
        eligible_stats.remove(worst_stat)

    # Return eligible stats
    return eligible_stats
    
def build_set(species, moves):

    # Get the base stats for the species
    base_stats = species["baseStats"]

    # Get the best nature for the species stats
    nature = get_best_nature(base_stats)

    # Get the best moves for the given species, nature
    best_moves = get_best_moves(moves, species, nature)[:4]

    # Get the best ev spread for the given moves, species, nature
    best_evs = get_best_evs(best_moves, base_stats, nature)

    print("Set generated:")
    print(f"{species['name']} @ (no item)")
    print(f"Nature: {nature}")
    print(f"EVs: {', '.join(best_evs)}")
    print(f"Moves:")
    for move in best_moves:
        print(f"- {move['name']}")

def get_species_set(species_json, species_moves):
    # Get the data for the species moves
    moves = parse_moves(species_moves)

    # Build the set for the given species
    set = build_set(species_json, moves)

def get_showdown_data(force=False):
    # Moves Data
    moves = {}

    # Create the data directory
    os.makedirs("data", exist_ok=True)

    # Moves Filename
    moves_file = os.path.join("data", "moves.json")

    # Force switch set, or moves file not present
    if force or not os.path.exists(moves_file):
        # Download the file from the server, and save it to the data folder
        request = requests.get("https://play.pokemonshowdown.com/data/moves.json")

        # Get json data
        content = request.content

        # Load moves from json data
        moves = JSON.loads(content)

        with open(moves_file, "w+") as file:
            # Write json data to file
            JSON.dump(moves, file)

    else:  # File already exists
        with open(moves_file, "r") as file:
            # Read json data from file
            moves = JSON.load(file)

    # Pokedex data
    dex = {}

    # Pokedex Filename
    dex_file = os.path.join("data", "pokedex.json")

    # Force switch set, or dex file not present
    if force or not os.path.exists(dex_file):
        # Download the file from the server, and save it to the data folder
        request = requests.get("https://play.pokemonshowdown.com/data/pokedex.json")

        # Get json data
        content = request.content

        # Load dex from json data
        dex = JSON.loads(content)

        with open(dex_file, "w+") as file:
            # Write json data to file
            JSON.dump(dex, file)

    else:  # File already exists
        with open(dex_file, "r") as file:
            # Read json data from file
            dex = JSON.load(file)

    # Return data
    return moves, dex


def convert_to_showdown_format(input_string, sep=""):
    # Use regular expression to split on uppercase characters (excluding the first one)
    words = re.findall(r"[A-Z][a-z]*", input_string)

    # Join the words with spaces and lower-case convert each word
    formatted_string = sep.join(word.lower() for word in words)

    # Return the formatted string
    return formatted_string


def convert_to_species_format(input_string):
    # Use regular expression to split on uppercase characters (excluding the first one)
    words = re.findall(r"[A-Z][a-z]*", input_string)

    # Join the words with underscores and capitalize each word
    formatted_string = "_".join(word.upper() for word in words)

    # Return with the "SPECIES_" prefix added
    return "SPECIES_" + formatted_string


if __name__ == "__main__":
    # Get showdown data files
    MOVES, POKEMON = get_showdown_data()

    # Get the arguments
    args = sys.argv[1:]

    # No arguments provided
    if len(args) == 0:
        # Use sample teachable learnsets file (generated by porymoves)
        args.append(os.path.join("input", "teachable_learnsets.h"))

    # Loop over arguments
    for filename in args:
        print(f"Processing file '{filename}' ...")

        # Attempt to open the file
        with open(filename, "r") as file:
            # Name Constants
            constant_species = None
            showdown_species = None

            # Data Constants
            species_moves = None
            species_json = None

            # Read the content from the file
            lines = file.readlines()

            # Read over the file
            for line in lines:
                # Line contains list declaration
                if "static const u16 s" in line:
                    # Get the species name from the line
                    raw_species = line[18:].split("TeachableLearnset")[0]

                    print(f"Processing species '{raw_species}' ...")

                    # Convert to header species constant format
                    constant_species = convert_to_species_format(raw_species)

                    # Convert to bulbapedia data extract format
                    showdown_species = convert_to_showdown_format(raw_species)

                    # Species is not found in the bulbapedia list
                    if not showdown_species in POKEMON:
                        # Handle hisuian species
                        if "hisuian" in showdown_species:
                            showdown_species = showdown_species.replace(
                                "hisuian", "hisui"
                            )

                        # Handle alolan species
                        elif "alolan" in showdown_species:
                            showdown_species = showdown_species.replace(
                                "alolan", "alola"
                            )

                        # Handle galarian species
                        elif "galarian" in showdown_species:
                            showdown_species = showdown_species.replace(
                                "galarian", "galar"
                            )

                            # Galarian special cases
                            if showdown_species in DATA.SPECIAL_CASES:
                                showdown_species = DATA.SPECIAL_CASES[showdown_species]

                        # If the bulbapedia species is in the special cases list
                        elif showdown_species in DATA.SPECIAL_CASES:
                            # Use the special case instead of the generic conversion
                            showdown_species = DATA.SPECIAL_CASES[showdown_species]

                    # If the species is found in the list
                    if showdown_species in POKEMON:
                        print(
                            f"Species data retrieved successfully: '{showdown_species}' ..."
                        )

                        # Get species json data
                        species_json = POKEMON[showdown_species]

                        # Allocate moves list
                        species_moves = []

                    else:  # Unable to find species data
                        print(
                            f"Unable to find data for species '{showdown_species}', skipping ..."
                        )

                        # Null moves list
                        species_moves = None
                else:  # Anything else
                    # Line is move data
                    if "MOVE_" in line:
                        # Moves array not null
                        if species_moves != None:
                            # Add move to moves list
                            species_moves.append(line.strip().replace(",", ""))

                    # Line is ending
                    if "};" in line:
                        # Generate the factory set for the species)
                        get_species_set(species_json, species_moves)
