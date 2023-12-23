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

# Spread Utils
# import src.spreadutils as sputils


def build_set(species, moves):
    # Get the best moves for the given species, nature
    best_moves = mvutils.get_best_moves(moves, species)[:4]

    """
    # Get the base stats for the species
    base_stats = species["baseStats"]

    # Get the best nature for the species stats
    nature = sputils.get_best_nature(base_stats)

    # Get the best ev spread for the given moves, species, nature
    best_evs = sputils.get_best_evs(best_moves, base_stats, nature)
    """

    # Build the set object
    species_set = {
        "species": species["name"],
        "item": None,
        "nature": None,  # nature,
        "evs": None,  # best_evs,
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
                    constant_species = utils.get_pokeemerald_format(raw_species)

                    # Convert to bulbapedia data extract format
                    showdown_species = utils.get_showdown_format(raw_species)

                    # Species is not found in the bulbapedia list
                    if not showdown_species in PS.POKEMON:
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
                    if showdown_species in PS.POKEMON:
                        print(
                            f"Species data retrieved successfully: '{showdown_species}' ..."
                        )

                        # Get species json data
                        species_json = PS.POKEMON[showdown_species]

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
                        # Generate the set for the species
                        species_set = build_set(species_json, species_moves)

                        # Add the set to the species list
                        pokemon_sets[raw_species] = species_set

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
