# Global Imports
import random

# Data File
import src.data as DATA

# Showdown Data
import src.showdown as PS

# Utility Functions Library
import src.utils as utils

# Config File
import config as CONFIG

def parse_move(move_name):

    # Convert the move name to showdown format
    name = utils.get_showdown_format(move_name[4:])

    # Move found
    if name in PS.MOVES:
        # Return move data
        return PS.MOVES[name]
    # Move not found
    if name not in PS.MOVES:
        print(f"Move not found: {name}")
    
    return None

def parse_moves(moves_list):
    # List of moves
    moves = []

    # Loop over all of the moves
    for move in moves_list:
        # Get the data for the move
        move_data = parse_move(move)

        # Move is not none
        if move_data != None:
            # Add it to the list
            moves.append(move_data)

    # Return moves list
    return moves

# 
def get_subsection_rating(section, self = False):

    # Default rating
    rating = 1

    """
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
    """

    # Move has flags
    if "flags" in section:
        # Iterate over the flags
        for flag in section["flags"]:
            # If the flag has a boost
            if flag in DATA.FLAG_BOOSTS:
                # Apply the rating boost
                rating *= DATA.FLAG_BOOSTS[flag]

    # If the move has a status
    if "status" in section:
        # Multiply the rating based on the status
        rating *= DATA.STATUS_BOOSTS[section["status"]]

    # Move heals the user
    if "heal" in section:
        heal = section["heal"]
        rating *= 1.0 + (heal[0] / heal[1])

    # Move drains the target
    if "drain" in section:
        drain = section["drain"]
        rating *= 1.0 + (drain[0] / drain[1])

    # Chance is defined
    if "chance" in section:
        # Multiply rating by odds (e.g. 30% = 0.3)
        rating *= (section["chance"] / 100)

    # Secondary status defined
    if "status" in section:
        # Get the boost defined for the status
        rating *= DATA.STATUS_BOOSTS[section["status"]]

    # Secondary boosts defined
    if "boosts" in section:
        for stat in section["boosts"]:
            # Add ~10% for 1x boost (~20% for 2x boost), etc.
            rating *= 1.0 + (abs(section["boosts"][stat]) / 10)

    # Volatile status defined
    if "volatileStatus" in section:
        rating *= 1.5 # 1.5x for volatile status

    # Return the rating
    return rating

def get_move_rating(move, species, off_ratio, offdef_ratio):
    # Base Rating
    rating = 1

    # Multiply rating by the accuracy
    rating *= move["accuracy"] / 100

    # Get the rating for generic sections
    rating *= get_subsection_rating(move)

    # If secondary effects are assigned and not none
    if "secondary" in move and move["secondary"] != None:
        rating *= get_subsection_rating(move["secondary"])

    # If self effects are assigned and not none
    if "self" in move and move["self"] != None:
        rating *= get_subsection_rating(move["self"], True)

    # Move category is status
    if move["category"] == "Status":
        # Move is one of the primary types
        if move["type"] in species["types"]:
            rating *= CONFIG.SAME_TYPE_STATUS_MULTIPLIER

        # Divide by offdef ratio
        rating /= offdef_ratio

    else:  # Move is offensive
        # Move is one of the primary types
        if move["type"] in species["types"]:
            rating *= CONFIG.SAME_TYPE_MULTIPLIER

        # If physical, multiply by ratio
        if move["category"] == "Physical":
            rating *= off_ratio

        # If special, divide by ratio
        if move["category"] == "Special":
            rating /= off_ratio

        # Multiply rating by base power
        rating *= move["basePower"] / 100

    # Get random move rating multiplier range
    range = CONFIG.RANDOM_MOVE_MULTIPLIER_RANGE

    # Range not null
    if range != None:
        # Generate a random modifier within the range
        modifier = random.uniform(range[0], range[1])

        # Apply the modifier to the rating
        rating *= modifier
        
    # Return rating
    return rating


def get_best_moves(moves, species):

    # Move ratings array
    move_ratings = []

    # Get the base stats for the species
    base_stats = species["baseStats"]

    # Get the offensive (atk/spa) ratio
    off_ratio = utils.get_atk_spa_ratio(base_stats)

    # Get the offensive/defensive ratio for the species
    offdef_ratio = utils.get_offensive_defensive_ratio(base_stats)

    print(
        f"Offensive/Defensive ratio: {round(offdef_ratio,2)}, off. ratio: {round(off_ratio,2)} ..."
    )

    # Loop over the moves
    for move in moves:

        # Get the data for the species moves
        move_data = parse_move(move)

        # Move data found
        if move_data:

            # Get the rating for the move
            rating = get_move_rating(move_data, species, off_ratio, offdef_ratio)

            # Add the move rating to the list
            move_ratings.append(
                {
                    "move": move,
                    "data": move_data, 
                    "rating": rating,
                }
            )

    # Sort the ratings from low to high
    move_ratings.sort(key=lambda x: x["rating"], reverse=True)

    # Best moves list
    best_moves = []

    # Loop over the rated moves
    for move in move_ratings:

        # Get the data for the move
        move_data = move["data"]

        # Assume best move
        best = True

        # Loop over the best moves
        for best_move in best_moves:

            # Get the data for the 'best' move
            best_data = best_move["data"]

            if (
                move_data["category"] == best_data["category"] and move_data["type"] == best_data["type"]
            ):
                best = False  # Worse move with same type/category

        # Best is still set
        if best == True:
            # Add to best moves list
            best_moves.append(move)

    # Return best moves
    return best_moves
