# ipa-tokenizer

IPA transcription tokenizer

## Usage example

```python
from ipa_tokenizer.tokenizer import tokenize

tokens = tokenize("ˈtoʊ.kən.aɪz", language="en")
print(tokens)
# ['t', 'oʊ', 'k', 'ə', 'n', 'aɪ', 'z']
```

## License

Copyright 2023 Levi Gruspe

[GPLv3 or later](./LICENSE).

## Attributions

This repository contains some data files that are derived from works that are licensed under [CC BY-SA 3.0 licenses][1].
The copyright of the original works belong to their authors.
[PHOIBLE 2.0][2] is by Steven Moran and Daniel McCloy.
[Wiktionary][3] is by its editors and contributors.

Derivative works:

- `tools/data/phoible.csv`
    + based on [PHOIBLE][2] (Glottocode and ISO639-3 code columns)
- `tools/data/wiktionary.txt`
    + based on [the Wiktionary language list][4]
- `ipa_tokenizer/inventories.csv`
    + based on [PHOIBLE][2]
- `ipa_tokenizer/languages.json`
    + based on [PHOIBLE][2] and [the Wiktionary language list][4]

These derivative works are made available under a [CC BY-SA 3.0 license][1].

[1]: https://creativecommons.org/licenses/by-sa/3.0/
[2]: https://phoible.org/
[3]: https://en.wiktionary.org
[4]: https://en.wiktionary.org/wiki/Wiktionary:List_of_languages,_csv_format
