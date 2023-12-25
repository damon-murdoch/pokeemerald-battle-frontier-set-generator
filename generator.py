# Global Imports
import json as JSON
import sys, os
import random

# Showdown Data
import src.showdown as PS

# Data File
import src.data as DATA

# Config File
import config as CONFIG

# Utils File
import src.utils as utils

# Move Utils
import src.moveutils as mvutils

# Spread utils
import src.spreadutils as sputils


def build_set(species, moves):
    # Get the best moves for the given species, nature
    best_moves = mvutils.get_best_moves(moves, species)

    # Get the best ev spread for the given moves, species, nature
    evs, nature = sputils.get_best_spread(best_moves, species)

    # Build the set object
    species_set = {
        "species": species["name"],
        "item": None,
        "nature": nature,
        "evs": evs,
        "moves": [move["move"] for move in best_moves],
    }

    # Return the set
    return species_set


if __name__ == "__main__":

    # Get rng seed from config
    SEED = CONFIG.RANDOM_SEED

    # Get the arguments
    args = sys.argv[1:]

    # No arguments provided
    if len(args) == 0:
        # Use sample teachable learnsets
        args.append(CONFIG.DEFAULT_FILE)

    # Starting argument
    arg_num = 0

    # Loop over arguments
    for filename in args:
        print(f"Processing file '{filename}' ...")

        # RNG Seed is not None
        if SEED != None:
            print(f"Using RNG seed from config: {SEED} ...")
            random.seed(SEED)

        # Attempt to open the file
        with open(filename, "r") as file:
            # Sets generated
            pokemon_sets = {}

            # Name Constants
            species_constant = None
            species_showdown = None

            # Data Constants
            species_moves = None
            species_json = None

            # Leftover species to process
            alternate_formes = []

            # Read the content from the file
            lines = file.readlines()

            print(f"Reading {len(lines)} lines ...")

            # Read over the file
            for line in lines:
                # Line contains list declaration
                if "static const u16 s" in line:
                    # Get the species name from the line
                    raw_species = line[18:].split("TeachableLearnset")[0]

                    print(f"Processing species '{raw_species}' ...")

                    # Convert to header species constant format
                    species_constant = utils.get_pokeemerald_format(raw_species)

                    # Convert to bulbapedia data extract format
                    species_showdown = utils.get_showdown_format(raw_species)

                    # Species is not found in the bulbapedia list
                    if not species_showdown in PS.POKEMON:
                        # Handle hisuian species
                        if "hisuian" in species_showdown:
                            species_showdown = species_showdown.replace(
                                "hisuian", "hisui"
                            )

                        # Handle alolan species
                        elif "alolan" in species_showdown:
                            species_showdown = species_showdown.replace(
                                "alolan", "alola"
                            )

                        # Handle galarian species
                        elif "galarian" in species_showdown:
                            species_showdown = species_showdown.replace(
                                "galarian", "galar"
                            )

                            # Galarian special cases
                            if species_showdown in DATA.SPECIAL_CASES:
                                species_showdown = DATA.SPECIAL_CASES[species_showdown]

                        # If the bulbapedia species is in the special cases list
                        elif species_showdown in DATA.SPECIAL_CASES:
                            # Use the special case instead of the generic conversion
                            species_showdown = DATA.SPECIAL_CASES[species_showdown]

                    # If the species is found in the list
                    if species_showdown in PS.POKEMON:
                        print(
                            f"Species data retrieved successfully: '{species_showdown}' ..."
                        )

                        # Get species json data
                        species_json = PS.POKEMON[species_showdown]

                        # Allocate moves list
                        species_moves = []

                    else:  # Unable to find species data
                        print(
                            f"Unable to find data for species '{species_showdown}', skipping ..."
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

                        # Sets per species is not none, and is set to a value of greater than 1
                        if CONFIG.SETS_PER_SPECIES != None and CONFIG.SETS_PER_SPECIES > 1:
                            for i in range(1, CONFIG.SETS_PER_SPECIES + 1):

                                # Build the set for the new forme
                                species_set = build_set(species_json, species_moves)

                                # Add the set to the species list (with number indicator)
                                pokemon_sets[f"{species_constant}_{i}"] = species_set
                        else:
                            # Generate the set for the species
                            species_set = build_set(species_json, species_moves)

                            # Add the set to the species list
                            pokemon_sets[species_constant] = species_set


                        # Species has other formes
                        if "otherFormes" in species_json:

                            # Loop over all of the formes
                            for forme in species_json["otherFormes"]:

                                # Add to the left-over list
                                alternate_formes.append({
                                    "name": forme,
                                    "moves": species_moves, 
                                    "showdown": utils.get_showdown_format(forme),
                                    "constant": utils.get_pokeemerald_format(forme),
                                })

                                # Will be processed after, if no duplicates are found

            print(f"File processed successfully. Handling {len(alternate_formes)} alternate formes ...")

            # Loop over all of the formes
            for forme in alternate_formes:

                # Get forme pretty name
                name = forme["name"]

                # Dereference showdown forme name
                showdown = forme["showdown"]

                # Pokeemerald constant forme name
                constant = forme["constant"]

                # Assume not seen
                new = True

                # Loop over the sets
                for set in pokemon_sets:
                    # Dereference current set data
                    set_data = pokemon_sets[set]
                    
                    # Set matches current species name
                    if name == set_data["species"]:
                        new = False
                        break
                
                # Sets not created yet
                if new == True:

                    # Showdown has data for this species
                    if showdown in PS.POKEMON:

                        print(f"Processing alternate forme {name} ...")

                        # Get the json data for the forme
                        forme_json = PS.POKEMON[forme["showdown"]]

                        # Sets per species is not none, and is set to a value of greater than 1
                        if CONFIG.SETS_PER_SPECIES != None and CONFIG.SETS_PER_SPECIES > 1:
                            for i in range(1, CONFIG.SETS_PER_SPECIES + 1):

                                # Build the set for the new forme
                                forme_set = build_set(forme_json, forme["moves"])

                                # Add the set to the species list (with number indicator)
                                pokemon_sets[f"{forme['constant']}_{i}"] = forme_set

                        else: # One set only
                            # Build the set for the new forme
                            forme_set = build_set(forme_json, forme["moves"])

                            # Add the set to the species list
                            pokemon_sets[forme["constant"]] = forme_set
                        
                    else: # No showdown data
                        print(f"No showdown data for forme {name}, skipping ...")
                else: # Sets already added
                    print(f"Already added sets for forme {name}, skipping ...")

            # Argument number greater than zero
            if arg_num > 0:
                CONFIG.OUT_FILENAME = f"battle_frontier_sets_{arg_num}.json"

            if not os.path.exists(CONFIG.OUT_FOLDER):
                # If it doesn't exist, create the folder
                os.makedirs(CONFIG.OUT_FOLDER)

            # Combine output filepath
            outpath = os.path.join(CONFIG.OUT_FOLDER, CONFIG.OUT_FILENAME)

            # Open the output file with write access
            with open(outpath, "w+") as out_file:
                print(f"Writing output to file '{outpath}' ...")

                # Dump the JSON content to the file
                out_file.write(
                    JSON.dumps(
                        pokemon_sets,
                        indent=CONFIG.JSON_INDENT,
                        sort_keys=CONFIG.JSON_SORT_KEYS,
                    )
                )

                print("Done.")

        # Increment arg number
        arg_num += 1
