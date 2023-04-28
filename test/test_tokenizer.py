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
