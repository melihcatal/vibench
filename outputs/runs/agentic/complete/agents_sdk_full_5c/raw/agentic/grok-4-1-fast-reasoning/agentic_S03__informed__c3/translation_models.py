from typing import Union, Sequence, Literal

TranslationInput = Union[str, Sequence[str]]
TagHandling = Literal["html", "xml"]

# DeepL-specific supported target languages (upper case)
SUPPORTED_TARGET_LANGUAGES = {
    "BG", "CS", "DA", "DE", "EL", "EN", "ES", "ET", "FI", "FR", "HU", "IT",
    "JA", "LT", "LV", "NB", "NL", "PL", "PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"
}