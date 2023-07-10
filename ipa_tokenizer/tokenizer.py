# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
# pylint: disable=invalid-name
"""IPA transcription tokenizer."""

from ipa_tokenizer.corrections import (
    create_preprocessing_table,
    create_tokenization_table,
)
from ipa_tokenizer.inventories import (
    get_phoible_inventories,
    get_tone_letters,
    sound_frequencies,
)
from ipa_tokenizer.languages import to_glottocode
from ipa_tokenizer.normalize import normalize_ipa


inventories = get_phoible_inventories()
phones = inventories["*"]
preprocessing_table = create_preprocessing_table()
default_corrections = create_tokenization_table()
frequencies = sound_frequencies(inventories)
tones = get_tone_letters()
modifiers = {"ˑ", "ː"}


class UnknownSymbol(Exception):
    """Raised when an unknown symbol is encountered during tokenization."""
    def __init__(self, unknown_symbol: str, transcription: str) -> None:
        super()
        self.unknown_symbol = unknown_symbol
        self.transcription = transcription


def score_guess(guess: str, inventory: set[str]) -> tuple[int, int]:
    """Assign a score to a guess.

    The score is meant to be used as a sort key for sorting guesses
    (lower-scoring guesses are prioritized).
    """
    # Prefer guesses that are in the inventory.
    first = int(guess not in inventory)

    # If the language isn't specified, assign score based on frequency.
    if inventory is phones:
        second = -frequencies.get(guess, -1)
        return (first, second)

    # If the language is specified, prefer the longest guess.
    return (first, -len(guess))


def candidate_tokens(ipa: str, inventory: set[str]) -> list[str]:
    """Return prefixes of IPA that are valid phones in some language.

    The result is sorted by priority (prefer prefixes in inventory, then prefer
    longer prefixes).
    """
    prefixes = [ipa[:i + 1] for i in range(len(ipa))]
    prefixes.sort(key=lambda guess: score_guess(guess, inventory))
    return prefixes


def _help_tokenize(
    ipa: str,
    corrections: dict[str, str] = default_corrections,
    inventory: set[str] = phones,
) -> tuple[bool, list[str]]:
    """Help tokenize IPA transcription.

    Returns `ok` and `tokens`.
    If `ok`, `tokens` is a list of tokens.
    If not, `tokens` is a list containing the symbol that caused the
    tokenization to fail.
    """
    # Base cases.
    if not ipa:
        return True, []
    if len(ipa) == 1:
        if ipa in corrections:
            return True, [corrections[ipa]]
        return (ipa in phones), [ipa]

    # Result to return if tokenization fails.
    result = [""]

    guesses = candidate_tokens(ipa, inventory)
    for guess in guesses:
        if (guess not in corrections) and (guess not in phones):
            result = [guess]
            continue

        n = len(guess)
        ok, rest = _help_tokenize(ipa[n:], corrections, inventory)
        if not ok:
            result = rest
            continue

        return True, [corrections.get(guess, guess), *rest]

    # No matches found.
    return False, result


def get_language_inventory(language: str) -> set[str]:
    """Return sound inventory for the language.

    `language` should be a Wiktionary language code.
    Special case: if `language = "*"`, returns a reference to the entire
    PHOIBLE sound inventory.
    """
    if language == "*":
        return phones

    result = set()
    for code in to_glottocode(language):
        result.update(inventories.get(code, set()))
    return result


def fix_vowel_length_modifiers(tokens: list[str]) -> None:
    """Drop vowel length modifiers that don't combine with preceding tokens.

    And reorder tokens so that vowel length modifiers precede token letters.
    """
    if not tokens:
        return

    if tokens[0] in modifiers:
        tokens[0] = ""

    # Move length modifiers before token letters.
    for i in range(1, len(tokens)):
        modifier = tokens[i]
        if modifier not in modifiers:
            continue

        j = i - 1
        while j >= 0 and tokens[j] in tones:
            tokens[j + 1] = tokens[j]
            j -= 1
        tokens[j + 1] = modifier

    for i in range(1, len(tokens)):
        modifier = tokens[i]
        if modifier not in modifiers:
            continue

        # Check if modifier combines with the preceding symbol.
        # If not, delete it.
        segment = tokens[i - 1] + modifier
        if segment in phones:
            tokens[i - 1] = segment
        tokens[i] = ""


def tokenize(
    ipa: str,
    language: str = "*",
    corrections: dict[str, str] = default_corrections,
) -> list[str]:
    """Tokenize IPA transcription into a list of tokens.

    Takes an optional Wiktionary `language` code.
    The tokenization algorithm will prioritize sounds that appear in the
    language.
    Raises an `UnknownSymbol` exception when an unknown symbol is encountered
    during tokenization.
    """
    ipa = normalize_ipa(ipa).translate(preprocessing_table)

    # Further processing.
    # ^X appears in zh Wiktionary transcriptions, but it's probably a bug.
    # ˣ is just a guess.
    # This substitution can also be done using correction tables, but this is
    # much faster.
    ipa.replace("^X", "ˣ")

    inventory = get_language_inventory(language)

    ipa = normalize_ipa(ipa)
    ok, tokens = _help_tokenize(ipa, corrections, inventory)
    if not ok:
        raise UnknownSymbol("".join(tokens), ipa)

    # Post-processing.
    fix_vowel_length_modifiers(tokens)

    # Corrections sometimes return an empty string.
    # Those empty strings should be filtered out.
    return [token for token in tokens if token]


__all__ = ["tokenize", "UnknownSymbol"]
