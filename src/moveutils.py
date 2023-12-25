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


def get_subsection_rating(section, self=False):
    # Default rating
    rating = 1

    # Move priority is defined
    if "priority" in section:
        # Move has positive priority
        if section["priority"] > 0:
            # Apply priority multiplier to the move
            rating *= 1 + section["priority"] * CONFIG.PRIORITY_MULTIPLIER

        # Negative priority is ignored

    # Move has flags
    if "flags" in section:
        # Iterate over the flags
        for flag in section["flags"]:
            # If the flag has a multipler
            if flag in CONFIG.FLAG_MULTIPLIERS:
                # Apply the multiplier
                rating *= CONFIG.FLAG_MULTIPLIERS[flag]

    # If the move has a status
    if "status" in section:
        # Multiply the rating based on the status
        rating *= CONFIG.STATUS_MULTIPLIERS[section["status"]]

    # Move heals the user
    if "heal" in section:
        heal = section["heal"]
        rating *= 1.0 + ((heal[0] / heal[1]))

    # Move drains the target
    if "drain" in section:
        drain = section["drain"]
        rating *= 1.0 + ((drain[0] / drain[1]))

    # Chance is defined
    if "chance" in section:
        # Multiply rating by odds (e.g. 30% = 0.3)
        rating *= 1.0 + (section["chance"] / 100)

    # Secondary boosts defined
    if "boosts" in section:
        for stat in section["boosts"]:
            # Get the stage the boost is for
            stage = section["boosts"][stat]

            # Apply positive changes for self-boosts
            if self == True:
                if stage > 0:
                    rating *= 1 + (
                        CONFIG.BOOST_MULTIPLIERS[stat]
                        * stage
                        * CONFIG.SELF_BOOST_MULTIPLIER
                    )
            else:
                # Apply boost for negative change
                if stage < 0:
                    rating *= 1 + abs(CONFIG.BOOST_MULTIPLIERS[stat] * stage)

    # Volatile status defined
    if "volatileStatus" in section:
        status = section["volatileStatus"]
        # Volatile status is in the list of modifiers
        if status in CONFIG.VOLATILE_STATUS_MULTIPLIERS:
            # Apply the volatile status modifier to the rating
            rating *= CONFIG.VOLATILE_STATUS_MULTIPLIERS[status]

    # If 'willCrit' is set to true in the move settings
    if "willCrit" in section and section["willCrit"] == True:
        rating *= CONFIG.CRIT_MULTIPLIERS[3]  # 100% Crit Chance
    # Otherwise, raised critical hit ratio defined
    elif "critRatio" in section:
        # Apply raised crit ratio bonus for the move
        rating *= CONFIG.CRIT_MULTIPLIERS[section["critRatio"]]

    # Return the rating
    return rating


def get_move_rating(move_name, move_data, species):
    # Base Rating
    rating = 1

    # Get the base stats for the species
    base_stats = species["baseStats"]

    # Get the offensive (atk/spa) ratio
    off_ratio = utils.get_atk_spa_ratio(base_stats)

    # Get the offensive/defensive ratio for the species
    offdef_ratio = utils.get_offensive_defensive_ratio(base_stats)

    # Move has a default rating
    if move_name in CONFIG.MOVE_MULTIPLIERS:
        # Get the default rating for the move
        rating = CONFIG.MOVE_MULTIPLIERS[move_name]

    # If doubles mode is disabled, and the move can only targets allies
    if CONFIG.DOUBLES_MODE == False and move_data["target"] == "adjacentAlly":
        rating = 0  # Cannot use move

    # If rating is non-zero
    if rating > 0:
        # Dereference move accuracy
        accuracy = move_data["accuracy"]

        # Accuracy check required
        if accuracy != True:
            # Multiply rating by the accuracy
            rating *= move_data["accuracy"] / 100

        # Get the target for the move
        target = move_data["target"]

        # Check if move is self-targeting
        self_target = target == "self"

        # Get the rating for generic sections
        rating *= get_subsection_rating(move_data, self_target)

        # Move targets both opponents / all other pokemon / partner
        if target in ["allAdjacent", "allAdjacentFoes", "allySide"]:
            # Multiply rating by doubles multiplier
            rating *= CONFIG.DOUBLES_MULTIPLIER

        # If secondary effects are assigned and not none
        if "secondary" in move_data and move_data["secondary"] != None:
            rating *= get_subsection_rating(move_data["secondary"], self_target)

        # If multiple secondary effects
        if "secondaries" in move_data:
            # Loop over all of the secondary effects
            for secondary in move_data["secondaries"]:
                # Apply rating change for each secondary effect
                rating *= get_subsection_rating(secondary, self_target)

        # Move category is status
        if move_data["category"] == "Status":
            # Move is one of the primary types
            if move_data["type"] in species["types"]:
                # Apply same-type status multiplier
                rating *= CONFIG.SAME_TYPE_STATUS_MULTIPLIER

            # Get the base speed stat for the species
            base_speed = base_stats["spe"]

            # Mon has lower than avg. speed
            if (
                base_speed < CONFIG.AVERAGE_SPEED
                and move_name in CONFIG.LOW_SPEED_MOVES
            ):
                rating *= (
                    1
                    + ((CONFIG.AVERAGE_SPEED - base_speed) / CONFIG.AVERAGE_SPEED)
                    * CONFIG.LOW_SPEED_MOVES[move_name]
                )

            # Higher than avg. speed
            elif (
                base_speed > CONFIG.AVERAGE_SPEED
                and move_name in CONFIG.HIGH_SPEED_MOVES
            ):
                rating *= (
                    1
                    + ((base_speed - CONFIG.AVERAGE_SPEED) / CONFIG.AVERAGE_SPEED)
                    * CONFIG.HIGH_SPEED_MOVES[move_name]
                )

            # If self effects are assigned and not none
            elif "self" in move_data and move_data["self"] != None:
                rating *= get_subsection_rating(move_data["self"], True)

                # Move has a volatile status
                if "volatileStatus" in move_data:
                    # Get the status from the move data
                    status = move_data["volatileStatus"]

                    # If move is a protecting move
                    if status in DATA.STATUS_PROTECT:
                        # Multiply ratio by offdef ratio - protect is preferred by frailer Pokemon
                        rating *= offdef_ratio
                    else:  # Non-protecting move
                        # Apply offdef ratio modifier normall
                        rating /= offdef_ratio
            else:
                # Apply offdef ratio modifier
                rating /= offdef_ratio

        else:  # Move is offensive
            # Get the type for the move
            move_type = move_data["type"]

            # Move is one of the primary types
            if move_type in species["types"]:
                # Apply same-type multiplier
                rating *= CONFIG.SAME_TYPE_MULTIPLIER
            else:  # Apply other type multiplier
                rating *= CONFIG.TYPE_MULTIPLIERS[move_type]

            # If physical, multiply by ratio
            if move_data["category"] == "Physical":
                if off_ratio > CONFIG.SPA_RATIO_CUTOFF:
                    rating *= off_ratio
                    # Apply offdef ratio modifier
                    rating *= offdef_ratio
                else:
                    # Apply ratio cutoff multiplier
                    rating = min(off_ratio, CONFIG.RATIO_CUTOFF_MULTIPLIER)

            # If special, divide by ratio
            if move_data["category"] == "Special":
                if off_ratio < CONFIG.ATK_RATIO_CUTOFF:
                    rating /= off_ratio
                    # Apply offdef ratio modifier
                    rating *= offdef_ratio
                else:
                    # Apply ratio cutoff multiplier
                    rating = min(1 - off_ratio, CONFIG.RATIO_CUTOFF_MULTIPLIER)

            # Move base power constant
            basePower = move_data["basePower"]

            # Multi hit in section
            if "multihit" in move_data:
                hits = 0  # Number of hits
                multihit = move_data["multihit"]

                if isinstance(multihit, list):
                    # Calculate the avg. number of hits
                    hits = sum(multihit) / len(multihit)
                else:
                    # Use coded number of hits
                    hits = multihit

                # Apply number of hits to base power
                basePower *= hits

                # Apply multi hit bonus to rating
                rating *= CONFIG.MULTI_HIT_MULTIPLIER

            # Multiply rating by base power
            rating *= basePower / 100

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

    # Loop over the moves
    for move in moves:
        # Get the data for the species moves
        move_data = parse_move(move)

        # Move data found
        if move_data:
            # Get the rating for the move
            rating = get_move_rating(move, move_data, species)

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

    # Has protecting move
    has_protect = False

    # Has redirection move
    has_redirect = False

    # Number of status moves
    status_moves = 0

    # Number of offensive moves
    offensive_moves = 0

    # Volatile statuses list
    volatile_statuses = []

    # Move types
    move_types = {}

    # Best moves list
    best_moves = []

    # Loop over the rated moves
    for move in move_ratings:
        # If best moves list
        # has four items, stop
        if len(best_moves) > 3:
            break

        # Get the move name
        move_name = move["move"]

        # Get the data for the move
        move_data = move["data"]

        # Get the type for the move
        move_type = move_data["type"]

        # Get the category for the move
        move_category = move_data["category"]

        # Move is a status move
        if move_category == "Status":
            if status_moves >= CONFIG.MAX_STATUS_MOVES:
                continue  # Too many status moves
        else:  # Move is an offensive move
            if offensive_moves >= CONFIG.MAX_ATTACK_MOVES:
                continue  # Too many offensive moves

        # If a same-type move limit is set
        if CONFIG.MAX_SAME_TYPE_MOVES != None:
            # If this move is in the move types table, and
            # we have already exceeded the max of this type
            if (
                move_type in move_types
                and move_types[move_type] >= CONFIG.MAX_SAME_TYPE_MOVES
            ):
                continue  # Exceeded move limit

        # Assume best move
        best = True

        # Loop over the best moves
        for best_move in best_moves:
            # Get the data for the 'best' move
            best_data = best_move["data"]

            # Current move is a status move
            if move_category == "Status":
                # Other move is also a status move
                if best_data["category"] == "Status":
                    # Both moves apply status conditions
                    if "status" in move_data and "status" in best_data:
                        best = False  # No multiple status moves
                        break
            else:  # Current move is physical/special
                if (
                    # Category, priority and type all match
                    move_category == best_data["category"]
                    and move_type == best_data["type"]
                    and move_data["priority"] == best_data["priority"]
                ):
                    # Move / best move targets
                    move_target = move_data["target"]
                    best_target = best_data["target"]

                    # Doubles mode is enabled
                    if CONFIG.DOUBLES_MODE == True:
                        if (
                            # If both the current move and best move are multi-target moves
                            move_target in DATA.MULTI_TARGET
                            and best_target in DATA.MULTI_TARGET
                        ) or (
                            # If both the current move and best move are single target moves
                            move_target in DATA.SINGLE_TARGET
                            and best_target in DATA.SINGLE_TARGET
                        ):
                            best = False  # Worse move with same type/category
                            break

                    else:  # Doubles mode is disabled
                        if (
                            move_target in DATA.OTHER_TARGET
                            and best_target in DATA.OTHER_TARGET
                        ):
                            best = False  # Worse move with same type/category
                            break

        # Best is set to true
        if best == True:
            # Run some last-minute checks

            # Move has a volatile status
            if "volatileStatus" in move_data:
                # Get volatile status from move data
                status = move_data["volatileStatus"]

                # If we already have a duplicate
                if status in volatile_statuses:
                    continue  # No duplicates

                # Move is one of the protecting moves (or fake out)
                if status in DATA.STATUS_PROTECT:
                    if has_protect:
                        continue  # Already have protecting move
                    else:
                        has_protect = True

                # Move is one of the redirect moves
                elif status in DATA.STATUS_REDIRECT:
                    if has_redirect:
                        continue  # Already have redirection
                    else:
                        has_redirect = True

            # Special handling for fake out
            elif move_name == "MOVE_FAKE_OUT":
                if has_protect:
                    continue  # Do not stack fake out with protect
                else:
                    has_protect = True

            # Add to best moves list
            best_moves.append(move)

            # Move is a status move
            if move_category == "Status":
                status_moves += 1  # Increment status moves
            else:  # Move is an offensive move
                offensive_moves += 1  # Increment offensive moves

            # If the move type is already in the list
            if move_type in move_types:
                # Increment the number of moves
                move_types[move_type] += 1
            else:
                # Set type counter to one
                move_types[move_type] = 1

    # Return best moves
    return best_moves
