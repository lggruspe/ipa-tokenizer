# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Map wiktionary language codes to Glottocodes."""

from argparse import ArgumentParser, Namespace
from csv import reader
from json import dumps
from pathlib import Path

from langcodes import standardize_tag


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    return parser.parse_args()


def read_wiktionary() -> dict[str, set[str]]:
    """Create mapping from Wiktionary to standardized language codes."""
    result: dict[str, set[str]] = {}
    path = Path(__file__).with_name("data") / "wiktionary.txt"
    with open(path, encoding="utf-8") as file:
        for line in file:
            code = line.strip()
            result.setdefault(code, set()).add(standardize_tag(code))
    return result


def missing_codes() -> dict[str, set[str]]:
    """Mapping of missing codes."""
    return {
        ## Codes from Glottolog
        "angu1242": {"awg"},
        "bula1255": {"wga", "yil"},     # Not sure which one...
        "dhud1236": {"ddr"},
        "lizu1234": {"ers"},
        "lowe1402": {"nwg"},
        "luth1234": {"xpj"},
        "mink1237": {"xxm"},
        "mith1236": {"rxw"},
        "ngum1253": {"xnm"},
        "nucl1729": {"taj", "tdg", "tge"},  # Not sure which one...
        "pall1243": {"pmd"},
        "wala1263": {"nlw"},
        "warr1257": {"gjm", "wkr"},
        "west2443": {"xww"},    # Not sure about this...
        "yinw1236": {"yxm"},

        ## Possibly mislabeled

        # PHOIBLE calls sout2770 Ngunawal, Glottolog calls it Ngarigo or Yuin.
        # https://en.wikipedia.org/wiki/Ngarigo_language
        # https://en.wikipedia.org/wiki/Ngunnawal_language
        "sout2770": {"xjt", "xni", "xrd", "xul"},

        # PHOIBLE calls djad1246 Jardwadjali, Glottolog calls it
        # Djadjawurrungic.
        # https://en.wikipedia.org/wiki/Wemba_Wemba_language
        # https://en.wikipedia.org/wiki/Djadjawurrung_language
        "djad1246": {"xww"},

        # PHOIBLE and Glottolog call gudj1237 Gudjal, but Wikipedia calls it
        # Warrongo.
        # https://en.wikipedia.org/wiki/Warrongo_language
        "gudj1237": {"gdc", "wrg"},

        # PHOIBLE calls kawa1290 Ogh Awarrangg/Unyjan, Glottolog calls it
        # Kawarrang-Ogh Undjan.
        # Wikipedia has an article for the Kunjen language, which might be
        # related.
        # https://en.wikipedia.org/wiki/Kunjen_language
        "kawa1290": {"kin", "olk"},

        # PHOIBLE calls ngin1247 Ngintait, Glottolog calls it Ngindadj.
        # Wikipedia has an article for the Yuyu language, which might be
        # related.
        # https://en.wikipedia.org/wiki/Yuyu_language
        "ngin1247": {"yxu"},

        # PHOIBLE calls tyan1235 Thaynakwithi, Glotollog calls it
        # Tyanngayt-Mamngayt-Ntrwangayt-Ntrangit.
        # Wikipedia has an article for the Awngthim language, which might be
        # related.
        # https://en.wikipedia.org/wiki/Awngthim_language
        "tyan1235": {"gwm"},


        # PHOIBLE calls vach1239 Eastern Khanty, Glottolog calls it Vach
        # Khanty.
        # Wikipedia has an article for the Khanty language, which might be
        # related.
        # https://en.wikipedia.org/wiki/Khanty_language
        "vach1239": {"kca"},

        # PHOIBLE and Glottolog call yadh1237 Yadhaykenu.
        # Wikipedia has an article for the Uradhi language, which might be
        # related.
        # https://en.wikipedia.org/wiki/Uradhi_language
        "yadh1237": {"amz", "avm", "urf", "yxm"},

        # PHOIBLE calls east2773 Dolakha Newar, Glottolog calls it Eastern
        # Newari.
        # Wikipedia has an article for the Newar language, which east2773 seems
        # to be a dialect of.
        # https://en.wikipedia.org/wiki/Dolakha_Newar_language
        # https://en.wikipedia.org/wiki/Newar_language
        "east2773": {"new"},

        # PHOIBLE and Glottlog call pisa1245 Pisamira.
        # Wikipedia has articles for Carapana and Tatuyo, which might be
        # related.
        # https://en.wikipedia.org/wiki/Carapana_language
        # https://en.wikipedia.org/wiki/Pisamira_language
        # https://en.wikipedia.org/wiki/Tatuyo_language
        "pisa1245": {"cbc", "tav"},

        # PHOIBLE and Glottolog call yulp1239 Yulparija, Wikipedia calls it
        # Yulparirra.
        # According to Wiktionary, it's also called Martu Wangka.
        # https://en.wikipedia.org/wiki/Martu_Wangka_dialect
        # https://en.wikipedia.org/wiki/Yulparirra_language
        "yulp1239": {"mpj"},

        ## Not found
        # cola1237
        # kera1256
        # yari1243
        # zhon1235
    }


def wiktionary_codes() -> dict[str, str]:
    """Return some pairings of Glottocodes to Wiktionary codes."""
    return {
        "fore1274": "syd-fne",
        "guwa1244": "aus-guw",
        "mbiy1238": "aus-mbi",
        "ngko1236": "aus-ngk",
    }


def read_phoible() -> dict[str, set[str]]:
    """Create mapping from standardized language codes to Glottocodes."""
    missing = missing_codes()
    later = wiktionary_codes()

    result: dict[str, set[str]] = {}
    path = Path(__file__).with_name("data") / "phoible.csv"
    with open(path, encoding="utf-8") as file:
        for glottocode, iso639_3 in reader(file):
            if glottocode in missing or glottocode in later:
                continue

            if glottocode == "NA":
                # Nothing to be done.
                continue
            if iso639_3 == "NA":
                iso639_3 = "und"
            tag = standardize_tag(iso639_3)
            result.setdefault(tag, set()).add(glottocode)

    # Insert missing codes.
    for glottocode, codes in missing.items():
        for iso639_3 in codes:
            tag = standardize_tag(iso639_3)
            result.setdefault(tag, set()).add(glottocode)
    return result


def join(
    left: dict[str, set[str]],
    right: dict[str, set[str]],
) -> dict[str, set[str]]:
    """Return the composition right[left]."""
    result: dict[str, set[str]] = {}
    for key, values in left.items():
        for value in values:
            if value not in right:
                continue
            result.setdefault(key, set()).update(right[value])
    return result


def create_language_mapping() -> dict[str, set[str]]:
    """Return mapping of Wiktionary codes to Glottocodes."""
    first = read_wiktionary()
    second = read_phoible()

    composition = join(first, second)
    for key, value in wiktionary_codes().items():
        composition.setdefault(value, set()).add(key)

    del composition["und"]
    return composition


def main(_: Namespace) -> None:
    """Script entrypoint."""
    result = dumps({
        key: sorted(value) for key, value in create_language_mapping().items()
    })
    print(result)


if __name__ == "__main__":
    main(parse_args())
