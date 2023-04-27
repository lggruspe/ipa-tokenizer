# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Language codes."""

from json import loads
from pathlib import Path
import typing as t


# languages.json is generated using tools/language_codes.py
codes = t.cast(
    dict[str, list[str]],
    loads(
        Path(__file__).with_name("languages.json").read_text(encoding="utf-8"),
    ),
)


def to_glottocode(iso639_3: str) -> list[str]:
    """Convert ISO639-3 language code to Glottocode.

    Returns a list of possible Glottocodes.
    If there are no possible translations, returns an empty list.
    """
    return codes.get(iso639_3, [])


__all__ = ["to_glottocode"]
