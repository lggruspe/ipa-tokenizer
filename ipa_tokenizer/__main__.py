# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Tokenize IPA transcriptions from CSV data."""

from argparse import ArgumentParser, Namespace
from csv import reader, writer
import sys

from ipa_tokenizer.tokenizer import tokenize, UnknownSymbol


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-s",
        "--silent",
        dest="silent",
        default=False,
        action="store_true",
        help="continue silently on error",
    )
    parser.add_argument(
        "-n",
        "--index",
        dest="index",
        type=int,
        default=[0],
        nargs=1,
        help="column index of IPA transcriptions (default: 0)",
    )
    parser.add_argument(
        "-l",
        "--language",
        dest="language_index",
        type=int,
        default=[None],
        nargs=1,
        help="column index of Wiktionary language code (default: None)",
    )
    args = parser.parse_args()
    args.index = args.index[0]
    args.language_index = args.language_index[0]
    return args


def main(args: Namespace) -> None:
    """Script entrypoint."""
    out = writer(sys.stdout)
    index = args.index
    language_index = args.language_index
    try:
        for row in reader(sys.stdin):
            try:
                ipa = row[index]
            except IndexError:
                sys.exit(f"index {index} out of range: {row}")

            try:
                language = (
                    "*" if language_index is None else row[language_index]
                )
            except IndexError:
                sys.exit(f"index {index} out of range: {row}")

            try:
                row[index] = " ".join(tokenize(ipa, language=language))
            except UnknownSymbol as exc:
                if args.silent:
                    continue

                symbol = exc.unknown_symbol
                transcription = exc.transcription
                msg = f"unexpected [{symbol}] in {transcription}: {row}"
                sys.exit(msg)
            out.writerow(row)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main(parse_args())
