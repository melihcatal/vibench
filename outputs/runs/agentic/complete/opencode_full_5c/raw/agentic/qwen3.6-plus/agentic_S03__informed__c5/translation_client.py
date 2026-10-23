import os
from deepl import Translator

DEEPL_API_KEY_ENV = "DEEPL_AUTH_KEY"
DEEPL_API_URL = "https://api.deepl.com/v2/translate"
DEEPL_FREE_API_URL = "https://api-free.deepl.com/v2/translate"

LANGUAGE_CODE_MAP = {
    "en": "EN",
    "zh": "ZH",
    "zh-cn": "ZH",
    "zh-tw": "ZH",
    "ja": "JA",
    "ko": "KO",
    "fr": "FR",
    "de": "DE",
    "es": "ES",
    "pt": "PT",
    "pt-br": "PT-BR",
    "it": "IT",
    "nl": "NL",
    "ru": "RU",
    "ar": "AR",
    "bg": "BG",
    "cs": "CS",
    "da": "DA",
    "el": "EL",
    "et": "ET",
    "fi": "FI",
    "hu": "HU",
    "id": "ID",
    "lv": "LV",
    "lt": "LT",
    "nb": "NB",
    "pl": "PL",
    "ro": "RO",
    "sk": "SK",
    "sl": "SL",
    "sv": "SV",
    "tr": "TR",
    "uk": "UK",
}


def load_deepl_config():
    api_key = os.environ.get(DEEPL_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"DeepL API key not found. Set the {DEEPL_API_KEY_ENV} environment variable."
        )
    is_free_tier = api_key.endswith(":fx")
    api_url = DEEPL_FREE_API_URL if is_free_tier else DEEPL_API_URL
    return {
        "api_key": api_key,
        "api_url": api_url,
        "is_free_tier": is_free_tier,
    }


def get_deepl_client() -> Translator:
    config = load_deepl_config()
    server_url = config["api_url"].replace("/v2/translate", "")
    return Translator(config["api_key"], server_url=server_url)


def normalize_language_code(code: str) -> str:
    if not code:
        return ""
    normalized = code.lower().strip()
    return LANGUAGE_CODE_MAP.get(normalized, normalized.upper())
