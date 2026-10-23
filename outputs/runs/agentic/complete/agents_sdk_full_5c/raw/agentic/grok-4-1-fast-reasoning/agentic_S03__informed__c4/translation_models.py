from typing import List

LANG_ALIASES = {
    "english": "en",
    "eng": "en",
    "spanish": "es",
    "spa": "es",
    "french": "fr",
    "ger": "de",
    "german": "de",
    "chinese": "zh",
    "japanese": "ja",
    "japanese": "ja",
    "korean": "ko",
    "russian": "ru",
}

def normalize_language(lang: str) -> str:
    """Normalize language code or name to standard code for Google Translate."""
    lang = lang.lower().strip()
    return LANG_ALIASES.get(lang, lang)
