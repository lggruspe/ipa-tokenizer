# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test IPA tokenizer."""

import pytest

from ipa_tokenizer.tokenizer import tokenize, UnknownSymbol


def test_tokenize_with_unknown_symbol() -> None:
    """UnknownSymbol should be raised if input has an unknown symbol."""
    with pytest.raises(UnknownSymbol):
        tokenize("%")


def test_tokenize_no_empty_string() -> None:
    """The resulting list of tokens shouldn't contain an empty string."""
    assert tokenize(" ") == []

    # \u032f is a combining inverted breve below, like in [ɐ̯].
    # The tokenizer should ignore it if it doesn't modify the previous symbol.
    assert tokenize("\u032f") == []
    assert tokenize("aɪ̯l") == ["a", "ɪ", "l"]


def test_tokenize_length_modifier() -> None:
    """Disallow standalone length modifier without raising an error."""
    assert tokenize("ˑ") == []
    assert tokenize("ː") == []
    assert tokenize("a") == ["a"]
    assert tokenize("aː") == ["aː"]


def test_tokenize_null() -> None:
    """Disallow null symbol ∅."""
    with pytest.raises(UnknownSymbol):
        tokenize("∅")


def test_tokenize_syllable_breaks() -> None:
    """Syllable breaks should be respected."""
    assert tokenize("ts", language="pl") == ["ts"]

    examples = ["tˈs", "tˌs", "t.s", "t s"]
    for example in examples:
        assert tokenize(example, language="pl") == ["t", "s"], example
