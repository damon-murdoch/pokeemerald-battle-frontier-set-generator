# Global Imports
import random

# Data File
import src.data as DATA

# Config File
import config as CONFIG

# Utils File
import src.utils as utils


def get_nature(inc, dec):
    # Loop over all of the natures
    for nature in DATA.NATURES:
        data = DATA.NATURES[nature]
        if data["inc"] == inc and data["dec"] == dec:
            return nature

    print(f"No nature found for stats {inc}, {dec} - Returning neutral nature")

    # No matching nature
    # Return random neutral nature
    return random.choice(["bashful", "docile", "hardy", "quirky", "serious"])


def get_best_stat(base_stats, allowed_stats=None, skip_hp=False):
    # Most important non-hp stat
    current_best_stat = None
    current_best_stat_value = None

    # Allowed stats not defined
    if allowed_stats == None:
        # Use all base stat keys
        allowed_stats = base_stats

    # Loop over the base stats
    for stat in allowed_stats:
        # Skip hp stat if set (for natures)
        if stat == "hp" and skip_hp:
            continue

        # Best stat value not assigned yet, or current stat is better
        if (
            current_best_stat_value == None
            or base_stats[stat] > current_best_stat_value
        ):
            # Update best stat
            current_best_stat_value = base_stats[stat]
            current_best_stat = stat

    # Return best stat
    return current_best_stat


def get_worst_stat(base_stats, allowed_stats=None, skip_hp=False):
    # Least important non-hp stat
    current_worst_stat = None
    current_worst_stat_value = None

    # Allowed stats not defined
    if allowed_stats == None:
        # Use all base stat keys
        allowed_stats = base_stats

    # Loop over the base stats
    for stat in allowed_stats:
        # Skip hp stat if set (for natures)
        if stat == "hp" and skip_hp:
            continue

        # Best stat value not assigned yet, or current stat is better
        if (
            current_worst_stat_value == None
            or base_stats[stat] < current_worst_stat_value
        ):
            # Update best stat
            current_worst_stat_value = base_stats[stat]
            current_worst_stat = stat

    # Return best stat
    return current_worst_stat


def get_best_nature(base_stats):
    # If these are set, current
    # best stats will not need
    # to be evaluated
    best_stat = None
    worst_stat = None

    # Placeholders
    best_stats = None
    worst_stats = None

    # Get offensive stat ratios
    off_ratio = utils.get_atk_spa_ratio(base_stats)

    # Get offensive/defensive ratio
    offdef_ratio = utils.get_offensive_defensive_ratio(base_stats)

    # If Pokemon is more offensively orientated
    if offdef_ratio > CONFIG.OFFDEF_RATIO_CUTOFF:
        # Boost offensive stats, reduce defensive
        best_stats = ["atk", "spa", "spe"]
        worst_stats = ["def", "spd"]
    else:
        # Boost defensive stats, reduce offensive
        best_stats = ["def", "spd", "spe"]
        worst_stats = ["atk", "spa"]

    # If the pokemon is within the mixed ratio
    if CONFIG.SPA_RATIO_CUTOFF <= off_ratio <= CONFIG.ATK_RATIO_CUTOFF:
        # If speed is an eligible stat
        if "spe" in best_stats:
            # If the average of both def, spdef are better than the speed stat
            if (base_stats["def"] + base_stats["spd"] / 2) > base_stats["spe"]:
                # Remove speed from eligible stats
                best_stats.remove("spe")
                worst_stats.append("spe")

            else:  # Get the worst of def, spdef
                if "def" in best_stats and base_stats["def"] < base_stats["spd"]:
                    # Remove def from eligible stats
                    best_stats.remove("def")
                    worst_stats.append("def")
                elif "spd" in best_stats and base_stats["spd"] < base_stats["def"]:
                    # Remove spd from eligible stats
                    best_stats.remove("spd")
                    worst_stats.append("spd")

    else:  # Not within mixed ratio
        # Pokemon attack ratio is higher, remove special attack
        if off_ratio > CONFIG.ATK_RATIO_CUTOFF and "spa" in best_stats:
            best_stats.remove("spa")
            # Fix reduced stat to spa
            worst_stat = "spa"

        # Pokemon special attack ratio is higher, remove attack
        elif off_ratio < CONFIG.SPA_RATIO_CUTOFF and "atk" in best_stats:
            best_stats.remove("atk")
            # Fix reduced stat to atk
            worst_stat = "atk"

    # Best stat not set
    if best_stat == None:
        best_stat = get_best_stat(base_stats, best_stats, skip_hp=True)

    # Best stat not set
    if worst_stat == None:
        worst_stat = get_worst_stat(base_stats, worst_stats, skip_hp=True)

    # Get the best nature for the given spread
    return get_nature(best_stat, worst_stat)


def get_best_evs(moves, base_stats, nature):
    # Eligible stats for investing in
    eligible_stats = ["hp", "atk", "def", "spa", "spd", "spe"]

    # Get whichever stat is reduced by the nature
    reduced_stat = DATA.NATURES[nature]["dec"]

    # Reduced stat is set
    if reduced_stat:  # Remove it
        eligible_stats.remove(reduced_stat)

    # Number of phys/spec moves
    moves_physical = 0
    moves_special = 0

    # Loop over the moves
    for move in moves:
        # If move is physical, increment physical counter
        if move["category"] == "Physical":
            moves_physical += 1
        # If move is special, implement special counter
        elif move["category"] == "Special":
            moves_special += 1

    # If there are no physical attacks, and atk is still eligible
    if moves_physical == 0 and "atk" in eligible_stats:
        eligible_stats.remove("atk")  # Remove it, no need

    # If there are no special attacks, and spa is still eligible
    if moves_special == 0 and "spa" in eligible_stats:
        eligible_stats.remove("spa")  # Remove it, no need

    # If both stats are still in eligible stats
    if "atk" in eligible_stats and "spa" in eligible_stats:
        # Attack is lower, remove attack stat
        if base_stats["atk"] < base_stats["spa"]:
            eligible_stats.remove("atk")
        else:  # SpA is lower, remove SpA stat
            eligible_stats.remove("spa")

    # Speed is still an eligible stat
    if "spe" in eligible_stats:
        if (
            # If defense is not in eligible stats, or speed is higher than defense
            "def" not in eligible_stats
            or base_stats["spe"] > base_stats["def"]
        ) and (  # Both conditions must be true
            # Of special defense is not eligible, or speed is higher than spdef
            "spd" not in eligible_stats
            or base_stats["spe"] > base_stats["spd"]
        ):
            # Remove def, spd from options
            for stat in ["hp", "def", "spd"]:
                # Remove stat if eligible
                if stat in eligible_stats:
                    eligible_stats.remove(stat)

        else:  # Not speed orientated
            # Remove speed from eligible stats
            eligible_stats.remove("spe")

    # While more than two eligible stats
    while len(eligible_stats) > 2:
        # Record worst stats
        worst_stat = None
        worst_stat_value = None

        # Loop over eligible stats
        for stat in eligible_stats:
            # Get the value from the stat
            value = base_stats[stat]

            # Stat is hp
            if stat == "hp":
                # Multiply by 1.5x
                value *= CONFIG.HP_MULTIPLIER

            else:  # Any other stat
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
