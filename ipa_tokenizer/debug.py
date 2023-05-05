# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test tokenizer and print statistics."""

from argparse import ArgumentParser, Namespace
from collections import Counter
from csv import reader
from logging import warning
from pathlib import Path
import typing as t

from ipa_tokenizer.tokenizer import tokenize, UnknownSymbol


Language: t.TypeAlias = str
Word: t.TypeAlias = str
Transcription: t.TypeAlias = str
Record: t.TypeAlias = tuple[Language, Word, Transcription]
Symbol: t.TypeAlias = str


class UnknownSymbolCounter:
    """Records most common symbol errors."""
    def __init__(self) -> None:
        self.symbol_counter: Counter[Symbol] = Counter()
        self.language_counters: dict[Symbol, Counter[Language]] = {}

    def record_error(self, language: Language, symbol: Symbol) -> None:
        """Record symbol error."""
        self.symbol_counter[symbol] += 1
        self.language_counters.setdefault(symbol, Counter())[language] += 1

    def summarize(
        self,
        max_symbols: int | None = None,
        max_languages: int | None = None,
    ) -> str:
        """Summarize most common errors.

        Simply returns an empty string if there are no errors.
        """
        if max_symbols is not None and max_symbols <= 0:
            return ""
        if not self.symbol_counter:
            return ""

        result = "Most common errors:\n"
        for symbol, count in self.symbol_counter.most_common(max_symbols):
            result += f"\t[{symbol}] {count}\n"
            counter = self.language_counters[symbol]
            for language, occurrence in counter.most_common(max_languages):
                result += f"\t\t{language} {occurrence}\n"
        return result


def load_tsv(path: Path) -> list[Record]:
    """Load transcriptions from a TSV file."""
    with open(path, encoding="utf-8") as file:
        rows = [
            t.cast(Record, tuple(row)) for row in reader(file, delimiter="\t")
        ]
    return rows


def debug(records: list[Record]) -> None:
    """Try to tokenize all transcriptions in records and print some stats."""
    counter = UnknownSymbolCounter()
    passed = 0
    failed = 0
    for language, word, ipa in records:
        try:
            tokenize(ipa, language)
            passed += 1
        except UnknownSymbol as exc:
            transcription = exc.transcription
            symbol = exc.unknown_symbol

            failed += 1
            warning(f"{language}\t{word}\t{ipa}\t>\t{transcription}\t{symbol}")
            counter.record_error(language, symbol)

    if summary := counter.summarize():
        warning(summary)

    score = passed / (passed + failed)
    warning(f"Score: {score}")


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "tsv",
        type=Path,
        help="path to TSV file (columns: language, word, transcription)",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    records = load_tsv(args.tsv)
    debug(records)


if __name__ == "__main__":
    main(parse_args())
