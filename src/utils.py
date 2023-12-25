# Global Imports
import re

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


def get_atk_spa_ratio(base_stats, nature="quirky"):
    # Get atk/spa ratio (atk > 1, spa < 1)
    return (base_stats["atk"] * DATA.NATURE_MODIFIERS[nature]["atk"]) / (
        base_stats["spa"] * DATA.NATURE_MODIFIERS[nature]["spa"]
    )

def get_def_spd_ratio(base_stats, nature="quirky"):
    # Get atk/spa ratio (atk > 1, spa < 1)
    return (base_stats["def"] * DATA.NATURE_MODIFIERS[nature]["def"]) / (
        base_stats["spd"] * DATA.NATURE_MODIFIERS[nature]["spd"]
    )

def get_offensive_defensive_ratio(base_stats, nature="quirky"):
    # Calculates roughly if the Pokemon is more offensive or defensive orientated, by comparing the average of the
    # defensive stats when compared to the highest of the Pokemon's special attack and regular attack stats.
    return max(
        base_stats["spa"] * DATA.NATURE_MODIFIERS[nature]["spa"],
        base_stats["atk"] * DATA.NATURE_MODIFIERS[nature]["atk"],
    ) / (
        (
            base_stats["hp"]
            + (base_stats["def"] * DATA.NATURE_MODIFIERS[nature]["def"])
            + (base_stats["spd"] * DATA.NATURE_MODIFIERS[nature]["spd"])
        )
        / 3
    )


def get_showdown_format(input_string, sep=""):
    # Use regular expression to split on uppercase characters (excluding the first one)
    words = re.findall(r"[A-Z][a-z]*", input_string)

    # Join the words with spaces and lower-case convert each word
    formatted_string = sep.join(word.lower() for word in words)

    # Return the formatted string
    return formatted_string


def get_pokeemerald_format(input_string):
    # Use regular expression to split on uppercase characters (excluding the first one)
    words = re.findall(r"[A-Z][a-z]*", input_string)

    # Join the words with underscores and capitalize each word
    formatted_string = "_".join(word.upper() for word in words)

    # Return with the "SPECIES_" prefix added
    return "SPECIES_" + formatted_string
