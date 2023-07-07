# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
# pylint: disable=too-many-lines
"""Correction tables."""

from ipa_tokenizer.normalize import normalize_ipa


def create_preprocessing_table() -> dict[int, str]:
    """Return rules for translating unknown symbols during preprocessing.

    The result is a translation table compatible with `str.translate`.
    """
    table = {
        ## Suprasegmentals not used by PHOIBLE
        "‿": "",    # linking

        # Some zh transcriptions seem to use '|' for alternate pronunciations,
        # so those transcriptions will be incorrectly tokenized :(
        # Suprasegmentals that PHOIBLE uses won't be excluded:
        # ː (long)
        # ˑ (half-long)
        # ă (the diacritic, which means extra-short)

        # Suprasegmentals that break syllables also won't be excluded.
        # They are handled during tokenization instead.
        # Examples:
        # | (minor (foot) group)
        # ‖ (major (intonation) group)
        # ˈ (primary stress)
        # ˌ (secondary stress)
        # . (syllable break)

        ## Other IPA symbols

        # PHOIBLE doesn't use ties.
        "\u0361": "",   # combining tie above like in t͡s
        "\u035c": "",   # combining tie below like in d͜z

        ## Non-IPA symbols

        # Some symbols that don't represent a sound appear in many IPA
        # transcriptions.
        "-": "",

        # In transcriptions in proto-languages, * means that the pronunciation
        # is unattested or hypothetical.
        "*": "",

        ## Diacritics

        # Syllabic diacritics
        # These normally go on top if the symbol has a descender, but PHOIBLE
        # always puts the syllabic diacritic below.
        # https://en.wikipedia.org/wiki/Syllabic_consonant
        "\u030d": "\u0329",     # ex: ŋ̍ -> ŋ̩

        # Retraction diacritics
        # PHOIBLE uses a minus sign below instead of a macron.
        "\u0331": "\u0320",     # ex: e̱ -> e̠

        # Voicelessness diacritics
        # PHOIBLE uses both ŋ̥ and ŋ̊, but simphones merges the two.
        # simphones does the same for other duplicate segments.
        # For consistency, we'll always put the diacritic below the consonant.
        "\u030a": "\u0325",     # ex: b̊ -> b̥

        ## Typographic substitutes

        # /ᴇ/ is sometimes used in Sinology and Koreanology.
        # See https://en.wikipedia.org/wiki/Mid_front_unrounded_vowel
        # This could also be an /ɛ̝/, but /e̞/ is the more represented
        # symbol on PHOIBLE.
        "ᴇ": "e̞",

        "g": "ɡ",

        # Prenasal consonants
        # https://en.wikipedia.org/wiki/Prenasalized_consonant#Transcription
        # We won't substitute ⁿ, because PHOIBLE uses it.
        # We do it instead during tokenization.
        "ᵐ": "m",
        "ᶬ": "ɱ",
        "ᶯ": "ɳ",
        "ᶮ": "ɲ",
        "ᵑ": "ŋ",
        "ᶰ": "ɴ",

        ## Approximations

        # /ɝ/ isn't in PHOIBLE, so let's replace it with a different r-colored
        # vowel.
        "ɝ": "ɚ",

        # Used in Egyptian Wiktionary transcriptions for unknown vowels.
        "V": "",

        # ˣ
        # The vast majority of Wiktionary transcriptions that contain this
        # symbol are in Finnish (only about a handful are not).
        # Apparently, this symbol has no phonetic value.
        # https://linguistics.stackexchange.com/a/44644
        "ˣ": "",

        ## Tones
        # These substitutions are probably inaccurate.
        # Read more:
        # https://en.wikipedia.org/wiki/Tone_(linguistics)#Phonetic_notation
        # https://en.wikipedia.org/wiki/Tone_contour#Transcription
        # https://en.wikipedia.org/wiki/Tone_letter#Chao_tone_letters_(IPA)
        # https://en.wikipedia.org/wiki/Tone_letter#IPA_tone_letters_in_Unicode
        # https://www.internationalphoneticassociation.org/content/full-ipa-chart

        # Level tones
        "\u030b": "˥",  # combing double acute accent a̋ -> extra-high tone
        "\u0301": "˦",  # combining acute accent á -> high tone
        "\u0304": "˧",  # combining macron ā -> mid tone
        "\u0300": "˨",  # combining grave accent à -> low tone
        "\u030f": "˩",  # combining double grave accent ȁ -> extra-low tone

        # Tone contours
        # Each diacritic below can represent many possible tone letters
        # (according to the Tone (linguistics) Wikipedia page).
        # We'll map each one to the most represented tone letter.
        "\u0302": "˦˨",     # circumflex accent â -> falling
        "\u1dc7": "˥˩",     # acute-macron a᷇ -> high falling
        "\u1dc6": "˧˨",     # macron-grave a᷆ -> low falling
        "\u030c": "˨˦",     # caron ǎ -> rising
        "\u1dc5": "˨˧",     # grave-macron a᷅ -> low rising
        "\u1dc4": "˧˥",     # macron-acute a᷄ -> high rising
        "\u1dc9": "˦˨˦",  # acute-grave-acute a᷉ -> dipping/falling-rising
        "\u1dc8": "˨˦˨",  # grave-acute-grave a᷈ -> peaking/rising-falling

        "ꜛ": "",    # "↑" is not in PHOIBLE :(
        "ꜜ": "↓",

        # Assume superscript numbers are Chao tone letters.
        # (It's possible that some transcriptions use a language-specific
        # notation.)
        # See https://en.wikipedia.org/wiki/Tone_letter#Numerical_values
        "¹": "˩",
        "²": "˨",
        "³": "˧",
        "⁴": "˦",
        "⁵": "˥",

        "1": "˩",
        "2": "˨",
        "3": "˧",
        "4": "˦",
        "5": "˥",

        "⁶": "˨",   # The same tone letter in Cantonese and Taiwanese Hokkien.
        "6": "˨",

        # ᴴ appears in some zh transcriptions but not in PHOIBLE.
        # We replace it with a high tone (more presented) instead of an
        # extra-high tone.
        # https://en.wikipedia.org/wiki/Tone_letter#Capital-letter_abbreviations
        "ᴴ": "˦",
        "ᴹ": "˧",
        "ᴸ": "˨",

        ## Not omitted

        # We'll let the tokenizer emit an error if it encounters any of these
        # symbols.

        # '
        # It's not clear what an apostrophe stands for in a transcription,
        # because it can mean a stress marker, an ejective, a glottal stop,
        # etc.
        # See https://w.wiki/6aDV (obsolete and nonstandard symbols)

        # …
        # This is sometimes used to stand for omitted parts of the
        # transcription.

        # E H K L P T U
        # These letters appear in zh transcriptions that aren't actually
        # transcriptions, but were picked up by kaikki.
    }
    return {
        ord(normalize_ipa(key)): normalize_ipa(value)
        for key, value in table.items()
    }


def create_tokenization_table() -> dict[str, str]:
    """Return rules for translating unknown symbols during tokenization."""
    # The tokenization table is used after preprocessing, so symbols that have
    # been deleted during preprocessing shouldn't appear in the keys of the
    # tokenization table (e.g. ᵑ -> ŋ).
    table = {
        ## Tied symbols
        # Some tied symbols that appear in Wiktionary transcriptions don't
        # appear in the PHOIBLE dataset. These are replaced by PHOIBLE segments
        # that look most similar and have the largest representation.
        # Since combining ties should have been removed during preprocessing,
        # they shouldn't be included here.

        # d͡ʒ
        # This appears in many languages. /d̠ʒ/ is the most similar looking
        # in PHOIBLE that's also the most highly represented.
        "dʒ": "d̠ʒ",
        "dʒxʼ": "d̠ʒxʼ",
        "dʒɾ": "d̠ʒɾ",
        "dʒʰ": "d̠ʒʰ",
        "dʒʱ": "d̠ʒʱ",
        "dʒʲ": "d̠ʒʲ",
        "dʒʷ": "d̠ʒʷ",
        "dʒʼ": "d̠ʒʼ",
        "dʒː": "d̠ʒː",
        "dʒˠ": "d̠ʒˠ",
        "dʒ̤": "d̠ʒ̤",
        "dʒ̤ː": "d̠ʒ̤ː",
        "n̠dʒ": "n̠d̠ʒ",
        "n̠dʒʷ": "n̠d̠ʒʷ",
        "n̠̩dʒ": "n̠̩d̠ʒ",
        "ˀdʒ": "ˀd̠ʒ",
        "ⁿdʒ": "ⁿd̠ʒ",

        # t͜ʃ
        # This appears in many languages. /t̠ʃ/ is the most similar looking
        # in PHOIBLE that's also the most highly represented.
        "tʃ": "t̠ʃ",
        "n̠tʃ": "n̠t̠ʃ",
        "n̠tʃɾ": "n̠t̠ʃɾ",
        "n̠tʃʰ": "n̠t̠ʃʰ",
        "n̠tʃʷ": "n̠t̠ʃʷ",
        "n̠tʃʼ": "n̠t̠ʃʼ",
        "n̠̥tʃ": "n̠̥t̠ʃ",
        "tʃx": "t̠ʃx",
        "tʃɾ": "t̠ʃɾ",
        "tʃʰ": "t̠ʃʰ",
        "tʃʰː": "t̠ʃʰː",
        "tʃʲ": "t̠ʃʲ",
        "tʃʲʰ": "t̠ʃʲʰ",
        "tʃʲː": "t̠ʃʲː",
        "tʃʷ": "t̠ʃʷ",
        "tʃʷʰ": "t̠ʃʷʰ",
        "tʃʷʼ": "t̠ʃʷʼ",
        "tʃʷː": "t̠ʃʷː",
        "tʃʼ": "t̠ʃʼ",
        "tʃʼː": "t̠ʃʼː",
        "tʃˀ": "t̠ʃˀ",
        "tʃˠ": "t̠ʃˠ",
        "tʃˤ": "t̠ʃˤ",
        "tʃˤʰ": "t̠ʃˤʰ",
        "tʃˤʼ": "t̠ʃˤʼ",
        "tʃ̰": "t̠ʃ̰",
        "tʃ̺": "t̠ʃ̺",
        "tʃ̺ʰ": "t̠ʃ̺ʰ",
        "tʃ͉": "t̠ʃ͉",
        "ʰtʃ": "ʰt̠ʃ",
        "ʰtʃʰ": "ʰt̠ʃʰ",
        "ʰtʃː": "ʰt̠ʃː",

        # tʃː is actually in PHOIBLE, but it might be an error
        "tʃː": "t̠ʃː",

        # d̠͡ʑ
        # This only appears in Bosnian Wiktionary transcriptions.
        # PHOIBLE doesn't have a Bosnian inventory, but Croatian has dʑ.
        "d̠ʑ": "dʑ",
        "d̠ʑʰ": "dʑʰ",
        "d̠ʑʱ": "dʑʱ",
        "d̠ʑʱː": "dʑʱː",
        "d̠ʑː": "dʑː",
        "d̠ʑᶣ": "dʑᶣ",
        "nd̠ʑ": "ndʑ",
        "ɲ̟d̠ʑ": "ɲ̟dʑ",
        "ʱd̠ʑ": "ʱdʑ",
        "ⁿd̠ʑ": "ⁿdʑ",

        # d̥͡s
        # Appears in Tosk Albanian and Bavarian Wiktionary transcriptions.
        # This segment doesn't appear in PHOIBLE, but since [d̥] is an
        # unvoiced [d], we'll treat it like a [t].
        "d̥s": "ts",
        "d̥sɦ": "tsɦ",
        "d̥sʰ": "tsʰ",
        "d̥sʰː": "tsʰː",
        "d̥sʲ": "tsʲ",
        "d̥sʲʰ": "tsʲʰ",
        "d̥sʲː": "tsʲː",
        "d̥sʷ": "tsʷ",
        "d̥sʷʰ": "tsʷʰ",
        "d̥sʷʼ": "tsʷʼ",
        "d̥sʷː": "tsʷː",
        "d̥sʼ": "tsʼ",
        "d̥sʼː": "tsʼː",
        "d̥sˀ": "tsˀ",
        "d̥sː": "tsː",
        "d̥sˠ": "tsˠ",
        "d̥sˤʰ": "tsˤʰ",
        "d̥s̪": "ts̪",
        "d̥s̰": "ts̰",
        "d̥s̺": "ts̺",
        "d̥s̻": "ts̻",
        "d̥s͇": "ts͇",
        "d̥s͇ʰ": "ts͇ʰ",
        "nd̥s": "nts",
        "nd̥sʰ": "ntsʰ",
        "nd̥sʼ": "ntsʼ",
        "ʰd̥s": "ʰts",
        "ʰd̥sʰ": "ʰtsʰ",
        "ʰd̥sʲ": "ʰtsʲ",
        "ʰd̥sː": "ʰtsː",
        "ʷʰd̥s": "ʷʰts",

        # œ͡ɛ
        # Appears in Buriat Wiktionary transcriptions.
        # PHOIBLE uses œ̞ɛ̞ instead.
        "œɛ": "œ̞ɛ̞",

        # ɯ͡ɤ
        # Appears in Dolgan and Sakha Wiktionary transcriptions.
        # Neither languages contain ɯ͡ɤ in their PHOIBLE inventories.
        # However, Gagauz contains /ɯ̯ɤ̞/, so we'll use that instead.
        "ɯɤ": "ɯ̯ɤ̞",

        # t͡θʼ
        # Appears in Slavey (not in PHOIBLE) and Salish languages (appears as
        # various languages in PHOIBLE), none of which contain the segment.
        # However, there's a similar looking segment /t̪θʼ/.
        "tθʼ": "t̪θʼ",

        # t͡θʰ
        # This segment doesn't appear in the PHOIBLE inventories for Salish
        # languages. The most similar looking segment is /t̪θʰ/.
        "tθʰ": "t̪θʰ",

        # t͡θ
        # Some Chadong/Chaodong words use this symbol, but PHOIBLE doesn't have
        # an inventory for Chadong.
        # The most similar looking segments are /t̪θ/ and /t̪θ̪/, but /t̪θ/
        # is used as the replacement, because it's more highly represented.
        "tθ": "t̪θ",

        # i͜y
        # Appears in Old English, which has no PHOIBLE inventory.
        # It's replaced with i̯y, which appears in the Danish inventory.
        "iy": "i̯y",

        # d͡ʐ
        # Appears mainly in Polish transcriptions.
        # This symbol is equivalent to ɖʐ, which does appear in the PHOIBLE
        # data.
        # https://en.wikipedia.org/wiki/Voiced_retroflex_affricate
        # (The Polish PHOIBLE inventory actually uses /ɖ̻ʐ̻/, but /ɖʐ/ is
        # much more highly represented in the dataset.
        "dʐ": "ɖʐ",
        "dʐʷ": "ɖʐʷ",
        "ɳdʐ": "ɳɖʐ",
        "ⁿdʐ": "ⁿɖʐ",

        # t͡ʂ
        # Appears mainly in Polish transcriptions.
        # This symbol is equivalent to ʈʂ.
        # https://en.wikipedia.org/wiki/Voiceless_retroflex_affricate
        "tʂʰ": "ʈʂʰ",
        "tʂʷ": "ʈʂʷ",
        "tʂː": "ʈʂː",
        "tʂ͇": "ʈʂ͇",
        "ɳtʂ": "ɳʈʂ",
        "ɳtʂʰ": "ɳʈʂʰ",
        "ʰtʂʰ": "ʰʈʂʰ",

        # tʂ and tʂʼ are actually in PHOIBLE as allophones, but this might
        # be an error.
        "tʂ": "ʈʂ",
        "tʂʼ": "ʈʂʼ",

        # d̥͡ʑ d͡ʑ̥
        # Appear mainly in Chinese transcriptions.
        # These are probably the same as tɕ (based on the IPA chart).
        # There's another segment /d̥ʑ̥/ in PHOIBLE, but it's less
        # represented than /tɕ/.
        "d̥ʑ": "tɕ",
        "dʑ̥": "tɕ",
        "dʑ̥ʰ": "tɕʰ",
        "dʑ̥ʰː": "tɕʰː",
        "dʑ̥ʷ": "tɕʷ",
        "dʑ̥ʼ": "tɕʼ",
        "dʑ̥ː": "tɕː",
        "dʑ̥ᶣ": "tɕᶣ",
        "d̥ʑʰ": "tɕʰ",
        "d̥ʑʰː": "tɕʰː",
        "d̥ʑʷ": "tɕʷ",
        "d̥ʑʼ": "tɕʼ",
        "d̥ʑː": "tɕː",
        "d̥ʑᶣ": "tɕᶣ",
        "ndʑ̥": "ntɕ",
        "nd̥ʑ": "ntɕ",
        "ɲ̟dʑ̥ʰ": "ɲ̟tɕʰ",
        "ɲ̟d̥ʑʰ": "ɲ̟tɕʰ",
        "ʰdʑ̥": "ʰtɕ",
        "ʰdʑ̥ʰ": "ʰtɕʰ",
        "ʰd̥ʑ": "ʰtɕ",
        "ʰd̥ʑʰ": "ʰtɕʰ",
        "ʷʰdʑ̥": "ʷʰtɕ",
        "ʷʰd̥ʑ": "ʷʰtɕ",
        "ⁿdʑ̥ʰ": "ⁿtɕʰ",
        "ⁿd̥ʑʰ": "ⁿtɕʰ",

        # ɖ͡ʐ̥
        # Appears in Chinese Wiktionary transcriptions but not in PHOIBLE.
        # Possible replacements are /ʈʂ/ and /ɖ̥ʐ̥/.
        # /ʈʂ/ is more represented on PHOIBLE, so we'll use that.
        "ɖʐ̥": "ʈʂ",
        "ɖʐ̥ʰ": "ʈʂʰ",
        "ɖʐ̥ʷ": "ʈʂʷ",
        "ɖʐ̥ʼ": "ʈʂʼ",
        "ɖʐ̥ː": "ʈʂː",
        "ɖʐ̥͇": "ʈʂ͇",     # The key has an invisible equals sign below.
        "ɳɖʐ̥": "ɳʈʂ",
        "ɳɖʐ̥ʰ": "ɳʈʂʰ",
        "ʰɖʐ̥ʰ": "ʰʈʂʰ",

        # ʑ̥
        # This appears in some zh transcriptions, but it's not in PHOIBLE.
        # We'll replace it with /ɕ/ (the unvoiced /ʑ/ in the IPA chart).
        "ʑ̥": "ɕ",
        "ʑ̥ʰ": "ɕʰ",
        "ʑ̥ʼ": "ɕʼ",
        "ʑ̥ː": "ɕː",
        "ʑ̥̟": "ɕ̟",       # The key has an invisible plus sign below.
        "ʑ̥̟ː": "ɕ̟ː",     # The key has an invisible plus sign below.
        "ʑ̥ᶣ": "ɕᶣ",
        "ʷʰʑ̥ʰ": "ʷʰɕʰ",

        ## Others

        # Some segments in Wiktionary transcriptions seem to be in the wrong
        # order.
        "χːˤ": "χˤː",
        "qχːˤ": "qχˤː",

        "χˤʷ": "χʷˤ",
        "χˤʷː": "χʷˤː",
        "qχˤʷ": "qχʷˤ",
        "qχˤʷʼ": "qχʷˤʼ",

        "ɡʲʷ": "ɡʷʲ",

        # ʼʲ -> ʲʼ
        "kʼʲ": "kʲʼ",
        "k̟ʼʲ": "k̟ʲʼ",
        "pʼʲ": "pʲʼ",
        "qʼʲ": "qʲʼ",
        "tʼʲ": "tʲʼ",
        "t̪s̪ʼʲ": "t̪s̪ʲʼ",
        "t̪ʼʲ": "t̪ʲʼ",
        "ɬʼʲ": "ɬʲʼ",
        "ɬ̪ʼʲ": "ɬ̪ʲʼ",

        # ʰʷ -> ʷʰ
        "qʰʷ": "qʷʰ",
        "tʰʷ": "tʷʰ",
        "tsʰʷ": "tsʷʰ",
        "kʰʷ": "kʷʰ",
        "kʰʷː": "kʷʰː",

        # ːʷ -> ʷː
        "kːʷ": "kʷː",
        "sːʷ": "sʷː",
        "tsːʷ": "tsʷː",

        # ʼʷ -> ʷʼ
        "kʼʷ": "kʷʼ",
        "kʼʷː": "kʷʼː",
        "qʼʷ": "qʷʼ",
        "qʼʷː": "qʷʼː",
        "tsʼʷ": "tsʷʼ",
        "tɕʼʷ": "tɕʷʼ",
        "tʼʷ": "tʷʼ",

        # ʰˠ -> ˠʰ
        "pʰˠ": "pˠʰ",

        # ʰʲ -> ʲʰ
        "kʰʲ": "kʲʰ",
        "tʰʲ": "tʲʰ",
        "pʰʲ": "pʲʰ",

        # ːʰ -> ʰː
        "kːʰ": "kʰː",
        "tːʰ": "tʰː",
        "ʈːʰ": "ʈʰː",
        "tʃːʰ": "t̠ʃʰː",

        # ːʱ -> ʱː
        "bːʱ": "bʱː",
        "d̪ːʱ": "d̪ʱː",

        # ːʼ -> ʼː
        "qχːʼ": "qχʼː",
        "tɬːʼ": "tɬʼː",
        "tʃːʼ": "t̠ʃʼː",
        "tːʼ": "tʼː",

        # Appears in zh transcriptions with tones.
        # This shouldn't be put in the preprocessing table, because it serves
        # as a separator between tone contours.
        "⁻": "",

        ## Prenasal consonants
        # ⁿ can be written as n.
        # https://en.wikipedia.org/wiki/Prenasalized_consonant#Transcription

        # ⁿd
        "ⁿdl": "ndl",
        "ⁿdr": "ndr",
        "ⁿdzʲ": "ndzʲ",
        "ⁿdzʷ": "ndzʷ",
        "ⁿdɾ": "ndɾ",
        "ⁿdʲ": "ndʲ",
        "ⁿdʷ": "ndʷ",
        "ⁿdː": "ndː",

        # ⁿd̥
        "ⁿd̥": "nt",
        "ⁿd̥lʼ": "ntlʼ",
        "ⁿd̥s": "nts",
        "ⁿd̥sʰ": "ntsʰ",
        "ⁿd̥sʼ": "ntsʼ",
        "ⁿd̥ɕ": "ntɕ",
        "ⁿd̥ɾ": "ntɾ",
        "ⁿd̥ʰ": "ntʰ",
        "ⁿd̥ʷ": "ntʷ",
        "ⁿd̥ʼ": "ntʼ",

        # ⁿɮ
        "ⁿɮ": "nɮ",

        # ⁿm
        "ⁿm": "nm",     # nm is in PHOIBLE but only as an allophone

        # ⁿs
        "ⁿs": "ns",
        "ⁿsɾ": "nsɾ",
        "ⁿsʷ": "nsʷ",

        # ⁿt
        "ⁿt": "nt",
        "ⁿtlʼ": "ntlʼ",
        "ⁿts": "nts",
        "ⁿtsʰ": "ntsʰ",
        "ⁿtsʼ": "ntsʼ",
        "ⁿtɕ": "ntɕ",
        "ⁿtɾ": "ntɾ",
        "ⁿtʰ": "ntʰ",
        "ⁿtʷ": "ntʷ",
        "ⁿtʼ": "ntʼ",

        # ⁿz
        "ⁿz": "nz",
        "ⁿzɾ": "nzɾ",
        "ⁿzʷ": "nzʷ",

        # m ɱ ɳ ɲ ŋ ɴ
        # ᵐ, ᵑ and the others have been substituted with m and ŋ during
        # preprocessing.
        "mb̥": "mp",
        "ŋɡ̥": "ŋk",

        ## Clicks
        # Clicks often have many different transcriptions.
        # https://w.wiki/6atN (IPA chart)

        # k͡ʘ Tenuis bilabial click
        # https://en.wikipedia.org/wiki/Tenuis_bilabial_click
        "ʘ": "kʘ",
        "ᵏʘ": "kʘ",
        "𐞥ʘ": "qʘ",

        "ᵏʘʰ": "kʘʰ",
        "ʘʰ": "kʘʰ",
        # NOTE PHOIBLE doesn't seem to have qʘʰ (aspirated bilabial click).

        "ʘh": "kʘh",
        "ᵏʘh": "kʘh",
        "ʘkxʼ": "kʘkxʼ",
        "ᵏʘkxʼ": "kʘkxʼ",
        "ʘx": "kʘx",
        "ᵏʘx": "kʘx",
        "ʘʔ": "kʘʔ",
        "ᵏʘʔ": "kʘʔ",

        "𐞥ʘʼ": "qʘʼ",

        # g͡ʘ Voiced bilabial click
        # https://en.wikipedia.org/wiki/Voiced_bilabial_click
        "ʘ̬": "ɡʘ",
        "ᶢʘ": "ɡʘ",

        "𐞒ʘ": "ɢʘ",

        "ʘ̬kʰ": "ɡʘkʰ",
        "ᶢʘkʰ": "ɡʘkʰ",
        "ʘ̬kxʼ": "ɡʘkxʼ",
        "ᶢʘkxʼ": "ɡʘkxʼ",
        "ʘ̬x": "ɡʘx",
        "ᶢʘx": "ɡʘx",

        # ŋ͡ʘ Nasal bilabial click
        # https://en.wikipedia.org/wiki/Nasal_bilabial_click
        "ʘ̃": "ŋʘ",
        "mʘ": "ŋʘ",
        # NOTE PHOIBLE doesn't seem to have nasal bilabial uvular clicks and
        # aspirated bilabial nasial clicks

        "ʔʘ̃": "ʔŋʘ",
        "ʔmʘ": "ʔŋʘ",
        "ˀʘ̃": "ʔŋʘ",
        "ˀmʘ": "ʔŋʘ",
        "ˀŋʘ": "ʔŋʘ",

        "m̥ʘ": "ŋ̥ʘ",

        # k͡ǀ Tenuis dental click
        # https://en.wikipedia.org/wiki/Tenuis_dental_click
        "kʇ": "kǀ",
        "ǀ": "kǀ",
        "ʇ": "kǀ",
        "ᵏǀ": "kǀ",
        "ᵏʇ": "kǀ",

        "qʇ": "qǀ",
        "𐞥ǀ": "qǀ",
        "𐞥ʇ": "qǀ",

        "kʇʰ": "kǀʰ",
        "ǀʰ": "kǀʰ",
        "ʇʰ": "kǀʰ",
        "ᵏǀʰ": "kǀʰ",
        "ᵏʇʰ": "kǀʰ",
        # NOTE PHOIBLE doesn't seem to have aspirated dental clicks (qǀʰ)

        "ᵏǀ͓": "kǀ͓",
        "ᵏǀ͓ˀ": "kǀ͓ˀ",
        "ᵏǀ͓ˠʰ": "kǀ͓ˠʰ",
        "ᵏǀ͓x": "kǀ͓x",
        "ᵏǀ͓ʰ": "kǀ͓ʰ",

        "kʇʼ": "kǀʼ",
        "ǀʼ": "kǀʼ",
        "ʇʼ": "kǀʼ",
        "ᵏǀʼ": "kǀʼ",
        "ᵏʇʼ": "kǀʼ",

        "kʇx": "kǀx",
        "ǀx": "kǀx",
        "ʇx": "kǀx",
        "ᵏǀx": "kǀx",
        "ᵏʇx": "kǀx",

        "ᵏǀ̪": "kǀ̪",

        "kʇʷ": "kǀʷ",
        "ǀʷ": "kǀʷ",
        "ʇʷ": "kǀʷ",
        "ᵏǀʷ": "kǀʷ",
        "ᵏʇʷ": "kǀʷ",

        "kʇʷʰ": "kǀʷʰ",
        "ǀʷʰ": "kǀʷʰ",
        "ʇʷʰ": "kǀʷʰ",
        "ᵏǀʷʰ": "kǀʷʰ",
        "ᵏʇʷʰ": "kǀʷʰ",

        "kʇh": "kǀh",
        "ǀh": "kǀh",
        "ʇh": "kǀh",
        "ᵏǀh": "kǀh",
        "ᵏʇh": "kǀh",

        "kʇkxʼ": "kǀkxʼ",
        "ǀkxʼ": "kǀkxʼ",
        "ʇkxʼ": "kǀkxʼ",
        "ᵏǀkxʼ": "kǀkxʼ",
        "ᵏʇkxʼ": "kǀkxʼ",

        "kʇʔ": "kǀʔ",
        "ǀʔ": "kǀʔ",
        "ʇʔ": "kǀʔ",
        "ᵏǀʔ": "kǀʔ",
        "ᵏʇʔ": "kǀʔ",

        "kʇʰʼ": "kǀʰʼ",
        "ǀʰʼ": "kǀʰʼ",
        "ʇʰʼ": "kǀʰʼ",
        "ᵏǀʰʼ": "kǀʰʼ",
        "ᵏʇʰʼ": "kǀʰʼ",

        "kʇxʼ": "kǀxʼ",
        "ǀxʼ": "kǀxʼ",
        "ʇxʼ": "kǀxʼ",
        "ᵏǀxʼ": "kǀxʼ",
        "ᵏʇxʼ": "kǀxʼ",

        "qʇʼ": "qǀʼ",
        "𐞥ǀʼ": "qǀʼ",
        "𐞥ʇʼ": "qǀʼ",

        # ɡ͡ǀ Voiced dental click
        # https://en.wikipedia.org/wiki/Voiced_dental_click
        "ǀ̬": "ɡǀ",
        "ɡʇ": "ɡǀ",
        "ʇ̬": "ɡǀ",
        "ᵈǀ": "ɡǀ",
        "ᶢǀ": "ɡǀ",
        "ᶢʇ": "ɡǀ",

        "ɢʇ": "ɢǀ",
        "𐞒ǀ": "ɢǀ",
        "𐞒ʇ": "ɢǀ",

        "ᵈǀ͓": "ɡǀ͓",
        "ᶢǀ͓": "ɡǀ͓",
        "ᵈ̤ǀ͓": "ɡ̤ǀ͓",
        "ᶢ̤ǀ͓": "ɡ̤ǀ͓",

        "ᵈǀ͓x": "ɡǀ͓x",
        "ᶢǀ͓x": "ɡǀ͓x",
        "ᵈ̰ǀ͓x": "ɡ̰ǀ͓x",
        "ᶢ̰ǀ͓x": "ɡ̰ǀ͓x",

        "ǀ̬x": "ɡǀx",
        "ɡʇx": "ɡǀx",
        "ʇ̬x": "ɡǀx",
        "ᵈǀx": "ɡǀx",
        "ᶢǀx": "ɡǀx",
        "ᶢʇx": "ɡǀx",

        "ǀ̬kʰ": "ɡǀkʰ",
        "ɡʇkʰ": "ɡǀkʰ",
        "ʇ̬kʰ": "ɡǀkʰ",
        "ᵈǀkʰ": "ɡǀkʰ",
        "ᶢǀkʰ": "ɡǀkʰ",
        "ᶢʇkʰ": "ɡǀkʰ",

        "ǀ̬kxʼ": "ɡǀkxʼ",
        "ɡʇkxʼ": "ɡǀkxʼ",
        "ʇ̬kxʼ": "ɡǀkxʼ",
        "ᵈǀkxʼ": "ɡǀkxʼ",
        "ᶢǀkxʼ": "ɡǀkxʼ",
        "ᶢʇkxʼ": "ɡǀkxʼ",

        "ǀ̬ʱ": "ɡǀʱ",
        "ɡʇʱ": "ɡǀʱ",
        "ʇ̬ʱ": "ɡǀʱ",
        "ᵈǀʱ": "ɡǀʱ",
        "ᶢǀʱ": "ɡǀʱ",
        "ᶢʇʱ": "ɡǀʱ",

        "ǀ̬xʼ": "ɡǀxʼ",
        "ɡʇxʼ": "ɡǀxʼ",
        "ʇ̬xʼ": "ɡǀxʼ",
        "ᵈǀxʼ": "ɡǀxʼ",
        "ᶢǀxʼ": "ɡǀxʼ",
        "ᶢʇxʼ": "ɡǀxʼ",

        "ɢʇqʰ": "ɢǀqʰ",
        "𐞒ǀqʰ": "ɢǀqʰ",
        "𐞒ʇqʰ": "ɢǀqʰ",

        "ɡ̤ʇ": "ɡ̤ǀ",
        "ᵈ̤ǀ": "ɡ̤ǀ",
        "ᶢ̤ǀ": "ɡ̤ǀ",
        "ᶢ̤ʇ": "ɡ̤ǀ",

        # ŋ͡ǀ Nasal dental click
        # https://en.wikipedia.org/wiki/Nasal_dental_click
        "nʇ": "ŋǀ",
        "ŋʇ": "ŋǀ",
        "ǀ̃": "ŋǀ",
        "ʇ̃": "ŋǀ",
        "ⁿǀ": "ŋǀ",
        "ⁿʇ": "ŋǀ",
        # NOTE PHOIBLE doesn't seem to have nasal dental uvular clicks and
        # aspirated dental nasal clicks

        "ʼŋʇ": "ʼŋǀ",
        "ʼǀ̃": "ʼŋǀ",
        "ʼʇ̃": "ʼŋǀ",
        "ʼⁿǀ": "ʼŋǀ",

        "ʔŋʇ": "ʔŋǀ",
        "ʔǀ̃": "ʔŋǀ",
        "ʔʇ̃": "ʔŋǀ",
        "ʔⁿǀ": "ʔŋǀ",

        "ˀŋǀ": "ʔŋǀ",
        "ˀŋʇ": "ʔŋǀ",
        "ˀǀ̃": "ʔŋǀ",
        "ˀʇ̃": "ʔŋǀ",
        "ˀⁿǀ": "ʔŋǀ",

        "ŋʇʱ": "ŋǀʱ",
        "ǀ̃ʱ": "ŋǀʱ",
        "ʇ̃ʱ": "ŋǀʱ",
        "ⁿǀʱ": "ŋǀʱ",

        "ŋ̤ʇ": "ŋ̤ǀ",
        "ⁿ̤ǀ": "ŋ̤ǀ",

        "ŋ̥ʇ": "ŋ̥ǀ",
        "ⁿ̥ǀ": "ŋ̥ǀ",

        "ⁿǀ͓": "ŋǀ͓",
        "ⁿ̥ǀ͓xˀ": "ŋ̥ǀ͓xˀ",
        "ⁿ̥ǀ͓ʰ": "ŋ̥ǀ͓ʰ",
        "ⁿ̥ǀ͓ˀ": "ŋ̥ǀ͓ˀ",

        "ⁿ̤ǀ͓": "ŋ̤ǀ͓",

        # k͡ǃ Tenuis alveolar click
        # https://en.wikipedia.org/wiki/Tenuis_alveolar_click
        "kʗ": "kǃ",
        "ǃ": "kǃ",
        "ʗ": "kǃ",
        "ʗ̥": "kǃ",
        "ᵏǃ": "kǃ",
        "ᵏʗ": "kǃ",

        "qʗ": "qǃ",
        "𐞥ǃ": "qǃ",
        "𐞥ʗ": "qǃ",
        # NOTE PHOIBLE doesn't seem to have aspirated alveolar clicks (qǃʰ).

        "kʗʰ": "kǃʰ",
        "ǃʰ": "kǃʰ",
        "ʗʰ": "kǃʰ",
        "ʗ̥ʰ": "kǃʰ",
        "ᵏǃʰ": "kǃʰ",
        "ᵏʗʰ": "kǃʰ",

        "ᵏǃ̠": "kǃ̠",
        "ᵏǃ̠ˀ": "kǃ̠ˀ",
        "ᵏǃ̠xʰ": "kǃ̠xʰ",
        "ᵏǃ̠ʰ": "kǃ̠ʰ",

        "ᵏǃ͓": "kǃ͓",
        "ᵏǃ̪": "kǃ̪",

        "kʗx": "kǃx",
        "ǃx": "kǃx",
        "ʗx": "kǃx",
        "ʗ̥x": "kǃx",
        "ᵏǃx": "kǃx",
        "ᵏʗx": "kǃx",

        "kʗxʰ": "kǃxʰ",
        "ǃxʰ": "kǃxʰ",
        "ʗxʰ": "kǃxʰ",
        "ʗ̥xʰ": "kǃxʰ",
        "ᵏǃxʰ": "kǃxʰ",
        "ᵏʗxʰ": "kǃxʰ",

        "kʗʼ": "kǃʼ",
        "ǃʼ": "kǃʼ",
        "ʗʼ": "kǃʼ",
        "ʗ̥ʼ": "kǃʼ",
        "ᵏǃʼ": "kǃʼ",
        "ᵏʗʼ": "kǃʼ",

        "kʗh": "kǃh",
        "ǃh": "kǃh",
        "ʗh": "kǃh",
        "ʗ̥h": "kǃh",
        "ᵏǃh": "kǃh",
        "ᵏʗh": "kǃh",

        "kʗkxʼ": "kǃkxʼ",
        "ǃkxʼ": "kǃkxʼ",
        "ʗkxʼ": "kǃkxʼ",
        "ʗ̥kxʼ": "kǃkxʼ",
        "ᵏǃkxʼ": "kǃkxʼ",
        "ᵏʗkxʼ": "kǃkxʼ",

        "kʗʔ": "kǃʔ",
        "ǃʔ": "kǃʔ",
        "ʗʔ": "kǃʔ",
        "ʗ̥ʔ": "kǃʔ",
        "ᵏǃʔ": "kǃʔ",
        "ᵏʗʔ": "kǃʔ",

        "kʗʰʼ": "kǃʰʼ",
        "ǃʰʼ": "kǃʰʼ",
        "ʗʰʼ": "kǃʰʼ",
        "ʗ̥ʰʼ": "kǃʰʼ",
        "ᵏǃʰʼ": "kǃʰʼ",
        "ᵏʗʰʼ": "kǃʰʼ",

        "kʗxʼ": "kǃxʼ",
        "ǃxʼ": "kǃxʼ",
        "ʗxʼ": "kǃxʼ",
        "ʗ̥xʼ": "kǃxʼ",
        "ᵏǃxʼ": "kǃxʼ",
        "ᵏʗxʼ": "kǃxʼ",

        "qʗʼ": "qǃʼ",
        "𐞥ǃʼ": "qǃʼ",
        "𐞥ʗʼ": "qǃʼ",

        # ɡ͡ǃ Voiced alveolar click
        # https://en.wikipedia.org/wiki/Voiced_alveolar_click
        "ǃ̬": "ɡǃ",
        "ɡʗ": "ɡǃ",
        "ʗ̬": "ɡǃ",
        "ᶢǃ": "ɡǃ",
        "ᶢʗ": "ɡǃ",

        "ɢʗ": "ɢǃ",
        "𐞒ǃ": "ɢǃ",
        "𐞒ʗ": "ɢǃ",

        "ǃ̬x": "ɡǃx",
        "ɡʗx": "ɡǃx",
        "ʗ̬x": "ɡǃx",
        "ᶢǃx": "ɡǃx",
        "ᶢʗx": "ɡǃx",

        "ᶢǃ̠": "ɡǃ̠",

        "ŋ̤ǃ̬": "ŋ̤ɡǃ",
        "ŋ̤ɡʗ": "ŋ̤ɡǃ",
        "ŋ̤ʗ̬": "ŋ̤ɡǃ",
        "ŋ̤ᶢǃ": "ŋ̤ɡǃ",
        "ŋ̤ᶢʗ": "ŋ̤ɡǃ",

        "ǃ̬kʰ": "ɡǃkʰ",
        "ɡʗkʰ": "ɡǃkʰ",
        "ʗ̬kʰ": "ɡǃkʰ",
        "ᶢǃkʰ": "ɡǃkʰ",
        "ᶢʗkʰ": "ɡǃkʰ",

        "ǃ̬kxʼ": "ɡǃkxʼ",
        "ɡʗkxʼ": "ɡǃkxʼ",
        "ʗ̬kxʼ": "ɡǃkxʼ",
        "ᶢǃkxʼ": "ɡǃkxʼ",
        "ᶢʗkxʼ": "ɡǃkxʼ",

        "ǃ̬ʱ": "ɡǃʱ",
        "ɡʗʱ": "ɡǃʱ",
        "ʗ̬ʱ": "ɡǃʱ",
        "ᶢǃʱ": "ɡǃʱ",
        "ᶢʗʱ": "ɡǃʱ",

        "ǃ̬xʼ": "ɡǃxʼ",
        "ɡʗxʼ": "ɡǃxʼ",
        "ʗ̬xʼ": "ɡǃxʼ",
        "ᶢǃxʼ": "ɡǃxʼ",
        "ᶢʗxʼ": "ɡǃxʼ",

        "ɢʗqʰ": "ɢǃqʰ",
        "𐞒ǃqʰ": "ɢǃqʰ",
        "𐞒ʗqʰ": "ɢǃqʰ",

        "ɡ̰ʗx": "ɡ̰ǃx",
        "ᶢ̰ǃx": "ɡ̰ǃx",
        "ᶢ̰ʗx": "ɡ̰ǃx",

        "ɡ̤ʗ": "ɡ̤ǃ",
        "ᶢ̤ǃ": "ɡ̤ǃ",
        "ᶢ̤ʗ": "ɡ̤ǃ",

        # ŋ͡ǃ Nasal alveolar click
        # https://en.wikipedia.org/wiki/Nasal_alveolar_click
        "ŋʗ": "ŋǃ",
        "ǃ̃": "ŋǃ",
        "ʗ̃": "ŋǃ",
        # NOTE PHOIBLE doesn't seem to have nasal alveolar uvular clicks and
        # aspirated alveolar nasal clicks.

        "ʼŋʗ": "ʼŋǃ",
        "ʼǃ̃": "ʼŋǃ",
        "ʼʗ̃": "ʼŋǃ",

        "ʔŋʗ": "ʔŋǃ",
        "ʔǃ̃": "ʔŋǃ",
        "ʔʗ̃": "ʔŋǃ",
        "ˀŋǃ": "ʔŋǃ",
        "ˀŋʗ": "ʔŋǃ",
        "ˀǃ̃": "ʔŋǃ",
        "ˀʗ̃": "ʔŋǃ",

        "ŋʗʼ": "ŋǃʼ",
        "ǃ̃ʼ": "ŋǃʼ",
        "ʗ̃ʼ": "ŋǃʼ",

        "ŋ̥ʗˀ": "ŋ̥ǃˀ",

        "ŋʗʱ": "ŋǃʱ",
        "ǃ̃ʱ": "ŋǃʱ",
        "ʗ̃ʱ": "ŋǃʱ",

        "ŋ̥ʗ": "ŋ̥ǃ",

        "ŋ̤ʗ": "ŋ̤ǃ",

        "ŋ̥ǃˀˠ": "ŋ̥ǃˠˀ",

        # k͡ǂ Tenuis palatal click
        # https://en.wikipedia.org/wiki/Tenuis_palatal_click
        "k⨎": "kǂ",
        "k𝼋": "kǂ",
        "ǂ": "kǂ",
        "ᵏǂ": "kǂ",
        "ᵏ⨎": "kǂ",
        "ᵏ𝼋": "kǂ",
        "⨎": "kǂ",
        "𝼋": "kǂ",

        "𐞥ǂ": "qǂ",
        "𐞥𝼋": "qǂ",
        # NOTE PHOIBLE doesn't seem to have aspirated palatal clicks (qǂʰ).

        "k⨎ʰ": "kǂʰ",
        "k𝼋ʰ": "kǂʰ",
        "ǂʰ": "kǂʰ",
        "ᵏǂʰ": "kǂʰ",
        "ᵏ⨎ʰ": "kǂʰ",
        "ᵏ𝼋ʰ": "kǂʰ",
        "⨎ʰ": "kǂʰ",
        "𝼋ʰ": "kǂʰ",

        "k⨎x": "kǂx",
        "k𝼋x": "kǂx",
        "ǂx": "kǂx",
        "ᵏǂx": "kǂx",
        "ᵏ⨎x": "kǂx",
        "ᵏ𝼋x": "kǂx",
        "⨎x": "kǂx",
        "𝼋x": "kǂx",

        "ǂ͓ˡ": "kǂ͓ˡ",
        "ᵏǂ͓ˡ": "kǂ͓ˡ",

        "ǂ͓ˡʰ": "kǂ͓ˡʰ",
        "ᵏǂ͓ˡʰ": "kǂ͓ˡʰ",

        "ǂ͓ˡx": "kǂ͓ˡx",
        "ᵏǂ͓ˡx": "kǂ͓ˡx",

        "k⨎h": "kǂh",
        "k𝼋h": "kǂh",
        "ǂh": "kǂh",
        "ᵏǂh": "kǂh",
        "ᵏ⨎h": "kǂh",
        "ᵏ𝼋h": "kǂh",
        "⨎h": "kǂh",
        "𝼋h": "kǂh",

        "k⨎kxʼ": "kǂkxʼ",
        "k𝼋kxʼ": "kǂkxʼ",
        "ǂkxʼ": "kǂkxʼ",
        "ᵏǂkxʼ": "kǂkxʼ",
        "ᵏ⨎kxʼ": "kǂkxʼ",
        "ᵏ𝼋kxʼ": "kǂkxʼ",
        "⨎kxʼ": "kǂkxʼ",
        "𝼋kxʼ": "kǂkxʼ",

        "k⨎ʔ": "kǂʔ",
        "k𝼋ʔ": "kǂʔ",
        "ǂʔ": "kǂʔ",
        "ᵏǂʔ": "kǂʔ",
        "ᵏ⨎ʔ": "kǂʔ",
        "ᵏ𝼋ʔ": "kǂʔ",
        "⨎ʔ": "kǂʔ",
        "𝼋ʔ": "kǂʔ",

        "𐞥ǂʼ": "qǂʼ",
        "𐞥𝼋ʼ": "qǂʼ",

        # ɡ͡ǂ Voiced palatal click
        # https://en.wikipedia.org/wiki/Voiced_palatal_click
        "ǂɡ": "ɡǂ",
        "ǂ̬": "ɡǂ",
        "ᶢǂ": "ɡǂ",

        "ǂɡ̤": "ɡ̤ǂ",
        "ᶢ̤ǂ": "ɡ̤ǂ",

        "𐞒ǂ": "ɢǂ",

        "ǂɡx": "ɡǂx",
        "ǂ̬x": "ɡǂx",
        "ᶢǂx": "ɡǂx",

        "ᶢǂ͓ˡ": "ɡǂ͓ˡ",
        "ᶢǂ͓ˡx": "ɡǂ͓ˡx",
        "ᶢ̰ǂ͓ˡx": "ɡ̰ǂ͓ˡx",

        "ǂɡkʰ": "ɡǂkʰ",
        "ǂ̬kʰ": "ɡǂkʰ",
        "ᶢǂkʰ": "ɡǂkʰ",

        "ǂɡkxʼ": "ɡǂkxʼ",
        "ǂ̬kxʼ": "ɡǂkxʼ",
        "ᶢǂkxʼ": "ɡǂkxʼ",

        "ǂɡ̰x": "ɡ̰ǂx",
        "ᶢ̰ǂx": "ɡ̰ǂx",

        "ᶢ̤ǂ͓ˡ": "ɡ̤ǂ͓ˡ",

        # ŋǂ Nasal palatal click
        # https://en.wikipedia.org/wiki/Nasal_palatal_click
        "ǂŋ": "ŋǂ",
        "ǂ̃": "ŋǂ",
        # NOTE PHOIBLE doesn't seem to have nasal palatal uvular clicks and
        # aspirated palatal nasal clicks.

        "ʔǂŋ": "ʔŋǂ",
        "ʔǂ̃": "ʔŋǂ",
        "ˀǂŋ": "ʔŋǂ",
        "ˀǂ̃": "ʔŋǂ",
        "ˀŋǂ": "ʔŋǂ",

        "ǂŋ̤": "ŋ̤ǂ",

        "ǂŋ̥": "ŋ̥ǂ",

        "ŋ̥ǂ͓ʰˡ": "ŋ̥ǂ͓ˡʰ",
        "ŋ̥ǂ͓ˀˡ": "ŋ̥ǂ͓ˡˀ",

        # k͡ǁ Tenuis lateral click
        # https://en.wikipedia.org/wiki/Tenuis_lateral_click
        "kʖ": "kǁ",
        "ǁ": "kǁ",
        "ʖ": "kǁ",
        "ᵏǁ": "kǁ",
        "ᵏʖ": "kǁ",

        "qʖ": "qǁ",
        "𐞥ǁ": "qǁ",
        "𐞥ʖ": "qǁ",

        "kʖʰ": "kǁʰ",
        "ǁʰ": "kǁʰ",
        "ʖʰ": "kǁʰ",
        "ᵏǁʰ": "kǁʰ",
        "ᵏʖʰ": "kǁʰ",
        # NOTE PHOIBLE doesn't seem to have aspirated lateral clicks (q͜ǁʰ).

        "ᵏǁ͓": "kǁ͓",
        "ᵏǁ͓ˀ": "kǁ͓ˀ",
        "ᵏǁ͓xʰ": "kǁ͓xʰ",
        "ᵏǁ͓ʰ": "kǁ͓ʰ",

        "kʖx": "kǁx",
        "ǁx": "kǁx",
        "ʖx": "kǁx",
        "ᵏǁx": "kǁx",
        "ᵏʖx": "kǁx",

        "kʖʼ": "kǁʼ",
        "ǁʼ": "kǁʼ",
        "ʖʼ": "kǁʼ",
        "ᵏǁʼ": "kǁʼ",
        "ᵏʖʼ": "kǁʼ",

        "kʖh": "kǁh",
        "ǁh": "kǁh",
        "ʖh": "kǁh",
        "ᵏǁh": "kǁh",
        "ᵏʖh": "kǁh",

        "kʖkxʼ": "kǁkxʼ",
        "ǁkxʼ": "kǁkxʼ",
        "ʖkxʼ": "kǁkxʼ",
        "ᵏǁkxʼ": "kǁkxʼ",
        "ᵏʖkxʼ": "kǁkxʼ",

        "kʖʔ": "kǁʔ",
        "ǁʔ": "kǁʔ",
        "ʖʔ": "kǁʔ",
        "ᵏǁʔ": "kǁʔ",
        "ᵏʖʔ": "kǁʔ",

        "kʖʰʼ": "kǁʰʼ",
        "ǁʰʼ": "kǁʰʼ",
        "ʖʰʼ": "kǁʰʼ",
        "ᵏǁʰʼ": "kǁʰʼ",
        "ᵏʖʰʼ": "kǁʰʼ",

        "kʖxʼ": "kǁxʼ",
        "ǁxʼ": "kǁxʼ",
        "ʖxʼ": "kǁxʼ",
        "ᵏǁxʼ": "kǁxʼ",
        "ᵏʖxʼ": "kǁxʼ",

        "qʖʼ": "qǁʼ",
        "𐞥ǁʼ": "qǁʼ",
        "𐞥ʖʼ": "qǁʼ",

        # ɡ͡ǁ Voiced lateral click
        # https://en.wikipedia.org/wiki/Voiced_lateral_click
        "ǁ̬": "ɡǁ",
        "ɡʖ": "ɡǁ",
        "ʖ̬": "ɡǁ",
        "ᶢǁ": "ɡǁ",
        "ᶢʖ": "ɡǁ",

        "ɢʖ": "ɢǁ",
        "𐞒ǁ": "ɢǁ",
        "𐞒ʖ": "ɢǁ",

        "ᶢǁ͓": "ɡǁ͓",

        "ǁ̬x": "ɡǁx",
        "ɡʖx": "ɡǁx",
        "ʖ̬x": "ɡǁx",
        "ᶢǁx": "ɡǁx",
        "ᶢʖx": "ɡǁx",

        "ǁ̬kʰ": "ɡǁkʰ",
        "ɡʖkʰ": "ɡǁkʰ",
        "ʖ̬kʰ": "ɡǁkʰ",
        "ᶢǁkʰ": "ɡǁkʰ",
        "ᶢʖkʰ": "ɡǁkʰ",

        "ǁ̬kxʼ": "ɡǁkxʼ",
        "ɡʖkxʼ": "ɡǁkxʼ",
        "ʖ̬kxʼ": "ɡǁkxʼ",
        "ᶢǁkxʼ": "ɡǁkxʼ",
        "ᶢʖkxʼ": "ɡǁkxʼ",

        "ǁ̬xʼ": "ɡǁxʼ",
        "ɡʖxʼ": "ɡǁxʼ",
        "ʖ̬xʼ": "ɡǁxʼ",
        "ᶢǁxʼ": "ɡǁxʼ",
        "ᶢʖxʼ": "ɡǁxʼ",

        "ɢʖqʰ": "ɢǁqʰ",
        "𐞒ǁqʰ": "ɢǁqʰ",
        "𐞒ʖqʰ": "ɢǁqʰ",

        "ɡ̤ʖ": "ɡ̤ǁ",
        "ᶢ̤ǁ": "ɡ̤ǁ",
        "ᶢ̤ʖ": "ɡ̤ǁ",


        # ŋ͡ǁ Nasal lateral click
        # https://en.wikipedia.org/wiki/Nasal_lateral_click
        "ŋʖ": "ŋǁ",
        "ǁ̃": "ŋǁ",
        "ʖ̃": "ŋǁ",
        # NOTE PHOIBLE doesn't seem to have nasal lateral uvular clicks and
        # aspirated lateral nasal clicks.

        "ʔŋʖ": "ʔŋǁ",
        "ʔǁ̃": "ʔŋǁ",
        "ʔʖ̃": "ʔŋǁ",
        "ˀŋǁ": "ʔŋǁ",
        "ˀŋʖ": "ʔŋǁ",
        "ˀǁ̃": "ʔŋǁ",
        "ˀʖ̃": "ʔŋǁ",

        "ŋʖʼ": "ŋǁʼ",
        "ǁ̃ʼ": "ŋǁʼ",
        "ʖ̃ʼ": "ŋǁʼ",

        "ŋ̤ʖ": "ŋ̤ǁ",

        "ŋ̥ʖ": "ŋ̥ǁ",

        ## Replacements

        # ᵊ only appears in PHOIBLE in allophones.
        # However, the languages that use these symbol in Wiktionary the most
        # (Hindi, Panjabi, Urdu) don't have phonemes in PHOIBLE that are
        # allophones with a segment that contains ᵊ.
        # Therefore, we'll substitute ᵊ with ə.
        "ᵊ": "ə",

        # About 90% of Wiktionary transcriptions that use ˀ are Chinese.
        # Most of the time, it appears at the beginning of a word, so we'll
        # replace it with /ʔ/.
        "ˀ": "ʔ",

        ## Unrecognized diacritics and modifiers
        # Simply ignore diacritics/modifiers if they don't combine with the
        # preceding symbol.
        # NOTE Don't add too many substitution rules to this section.

        # Length modifiers
        # Match ː and ˑ even if they're not valid IPA segments. We'll fix
        # them during post-processing.
        "ː": "ː",
        "ˑ": "ˑ",

        # Non-syllabic
        "\u032f": "",   # combining inverted breve below like in [ɐ̯].

        # Syllabic
        "\u0329": "",   # combining vertical line below like in /n̩/.
        # NOTE There may be exceptions to this rule.
        # For example, isn't a syllabic /j/ just /i/?
        # https://linguistics.stackexchange.com/questions/40209/are-there-any-languages-that-have-syllabic-w-or-j

        # Suprasegmentals that break syllables
        # These aren't removed during preprocessing, because they are needed,
        # for instance, to distinguish between [t͡s] and [t.s].
        "|": "",    # minor (foot) group
        "‖": "",    # major (intonation) group
        "ˈ": "",    # primary stress
        "ˌ": "",    # secondary stress
        ".": "",    # syllable break
        " ": "",
    }
    return {
        normalize_ipa(key): normalize_ipa(value)
        for key, value in table.items()
    }


__all__ = ["create_preprocessing_table", "create_tokenization_table"]
