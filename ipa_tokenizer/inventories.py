# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""PHOIBLE sound inventories."""

from collections import Counter
from csv import reader
from pathlib import Path

from ipa_tokenizer.normalize import normalize_ipa


def get_phoible_inventories() -> dict[str, set[str]]:
    """Get PHOIBLE sound inventories.

    Keys are Glottocodes and values are set of sounds.
    There are three special keys:

    - * (combined inventory of all languages)
    - Djindewal (doesn't have a Glottocode)
    - ModernAramaic (doesn't have a Glottocode)
    """
    combined = set()
    result: dict[str, set[str]] = {}
    path = Path(__file__).with_name("inventories.csv")
    with open(path, encoding="utf-8") as file:
        for glottocode, sounds in reader(file):
            inventory = {normalize_ipa(sound) for sound in sounds.split()}

            # Remove standalone ː
            inventory.discard("ː")

            combined.update(inventory)
            result.setdefault(glottocode, set()).update(inventory)
    result["*"] = combined
    return result


def sound_frequencies(inventories: dict[str, set[str]]) -> Counter[str]:
    """Compute how many languages each sound occurs in."""
    counter: Counter[str] = Counter()
    for language, inventory in inventories.items():
        if language == "*":
            continue
        for sound in inventory:
            counter[sound] += 1
    return counter


__all__ = ["get_phoible_inventories", "sound_frequencies"]
