from typing import Set, Dict, Any

SUPPORTED_DEEPL_LANGUAGES: Set[str] = {
    "EN",
    "DE",
    "FR",
    "ES",
    "IT",
    "PT",
    "NL",
    "PL",
    "RU",
    "JA",
    "ZH",
    "BG",
    "CS",
    "DA",
    "EL",
    "ET",
    "FI",
    "HU",
    "LT",
    "LV",
    "RO",
    "SK",
    "SL",
    "SV",
    "TR",
}


def normalize_language_code(lang: str) -> str:
    return lang.upper().replace("-", "").replace("_", "")


def is_valid_deepl_language(lang: str) -> bool:
    return normalize_language_code(lang) in SUPPORTED_DEEPL_LANGUAGES


def build_translation_request(
    text: str, source_lang: str = "EN", target_lang: str = "DE"
) -> Dict[str, Any]:
    return {
        "text": [text],
        "source_lang": source_lang,
        "target_lang": target_lang,
    }


def parse_single_translation_response(response) -> str:
    return response.result.text
