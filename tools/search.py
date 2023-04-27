# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Search for words that use a string of symbols in its transcription."""

from argparse import ArgumentParser, Namespace
from csv import reader, writer
from pathlib import Path
import re
import sys


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "wordlist",
        type=Path,
        help="wordlist CSV file with language, word and transcription",
    )
    parser.add_argument(
        "substring",
        type=str,
        help="IPA substring to search for (unicode format: '\\uXXXX')",
    )
    parser.add_argument(
        "--no-language",
        dest="language",
        default=True,
        action="store_false",
        help="hide language",
    )
    parser.add_argument(
        "--no-word",
        dest="word",
        default=True,
        action="store_false",
        help="hide word",
    )
    parser.add_argument(
        "--no-transcription",
        dest="transcription",
        default=True,
        action="store_false",
        help="hide transcription",
    )
    return parser.parse_args()


def parse_substring(substring: str) -> str:
    """Parse IPA substring.

    Decodes unicode escapes.
    """
    pattern = r"\\u([0-9a-fA-F]{4})"
    return re.sub(
        pattern,
        lambda m: chr(int(f"0x{m.group(1)}", base=16)),
        substring,
    )


def main(args: Namespace) -> None:
    """Script entrypoint."""
    substring = parse_substring(args.substring)

    out = writer(sys.stdout)
    with open(args.wordlist, encoding="utf-8") as file:
        for language, word, transcription in reader(file):
            if substring in transcription:
                record = []
                if args.language:
                    record.append(language)
                if args.word:
                    record.append(word)
                if args.transcription:
                    record.append(transcription)
                out.writerow(record)


if __name__ == "__main__":
    main(parse_args())
