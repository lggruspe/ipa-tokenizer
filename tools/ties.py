# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Print the most common tied symbol pairs."""

from argparse import ArgumentParser, Namespace
from collections import Counter
from csv import reader
from pathlib import Path
import re


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "wordlist",
        type=Path,
        help="wordlist CSV file with language, word and transcription",
    )
    parser.add_argument(
        "context_size",
        default=1,
        type=int,
        nargs="?",
        help="number of symbols around tie to include as context (default: 1)",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    context = "." * args.context_size
    pattern = re.compile(rf"{context}(?:\u0361|\u035c){context}")

    counter: Counter[str] = Counter()
    with open(args.wordlist, encoding="utf-8") as file:
        for _, _, transcription in reader(file):
            for result in pattern.findall(transcription):
                counter[result] += 1

    for context, count in counter.most_common():
        print(context, count, sep="\t")


if __name__ == "__main__":
    main(parse_args())
