# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
# pylint: disable=redefined-outer-name
"""Test correction tables."""

import typing as t

import pytest

from ipa_tokenizer.corrections import (
    create_preprocessing_table,
    create_tokenization_table,
)
from ipa_tokenizer.inventories import get_phoible_inventories


@pytest.fixture
def phoible() -> set[str]:
    """Return PHOIBLE sounds."""
    inventories = get_phoible_inventories()
    return inventories["*"]


@pytest.fixture
def preprocessing_table() -> dict[int, str]:
    """Return preprocessing table."""
    return create_preprocessing_table()


@pytest.fixture
def tokenization_table() -> dict[str, str]:
    """Return tokenization table."""
    return create_tokenization_table()


def symbols(collection: t.Iterable[str]) -> set[str]:
    """Return set of symbols/characters used in collection of strings."""
    result: set[str] = set()
    for item in collection:
        result.update(item)
    return result


@pytest.fixture
def glyphs(phoible: set[str]) -> set[str]:
    """Return glyphs used by PHOIBLE."""
    return symbols(phoible)


def test_preprocessing_table_keys(
    preprocessing_table: dict[int, str],
    glyphs: set[str],
) -> None:
    """Keys should not be in any PHOIBLE inventory."""
    for key in preprocessing_table:
        for glyph in chr(key):
            assert glyph not in glyphs


def test_preprocessing_table_values(
    preprocessing_table: dict[int, str],
    glyphs: set[str],
    phoible: set[str],
) -> None:
    """Values should be in a PHOIBLE inventory as a glyph or as a sound."""
    for value in preprocessing_table.values():
        if value == "":
            continue

        assert value in glyphs or value in phoible


def test_tokenization_table_keys(
    tokenization_table: dict[str, str],
    phoible: set[str],
) -> None:
    """Keys should not be in PHOIBLE."""
    # Note that the inventory the tokenizer uses has removed invalid segments
    # like [tʂ], [tʂʼ], [tʃː].
    for key in tokenization_table:
        assert key not in phoible


def test_tokenization_table_values(
    tokenization_table: dict[str, str],
    phoible: set[str],
) -> None:
    """Values should be in PHOIBLE."""
    for value in tokenization_table.values():
        if value == "":
            continue
        assert value in phoible


def test_preprocessing_table_redundant_keys(
    preprocessing_table: dict[int, str],
) -> None:
    """Key shouldn't be the same as the replacement value."""
    for key, value in preprocessing_table.items():
        assert chr(key) != value


def test_tokenization_table_redundant_keys(
    tokenization_table: dict[str, str],
) -> None:
    """Key shouldn't be the same as the replacement value."""
    for key, value in tokenization_table.items():
        assert key != value


def test_redundant_keys(
    preprocessing_table: dict[int, str],
    tokenization_table: dict[str, str],
) -> None:
    """If a glyph gets substituted during preprocessing, it shouldn't appear in
    the tokenization table keys.
    """
    first = symbols(map(chr, preprocessing_table.keys()))
    second = symbols(tokenization_table.keys())
    for glyph in first:
        assert glyph not in second

    for key, value in tokenization_table.items():
        assert key != value
