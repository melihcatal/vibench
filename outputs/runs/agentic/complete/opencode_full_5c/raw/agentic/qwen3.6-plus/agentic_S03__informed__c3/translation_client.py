import os
from typing import Optional
import deepl


def load_deepl_config() -> dict:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable is required for DeepL API access"
        )

    api_url = os.environ.get("DEEPL_API_URL", "https://api.deepl.com/v2")
    is_free_tier = os.environ.get("DEEPL_FREE_TIER", "false").lower() == "true"

    if is_free_tier:
        api_url = "https://api-free.deepl.com/v2"

    return {
        "auth_key": auth_key,
        "api_url": api_url,
        "is_free_tier": is_free_tier,
    }


def get_translation_client() -> deepl.Translator:
    config = load_deepl_config()
    server_url = config["api_url"] if not config["is_free_tier"] else None
    client = deepl.Translator(
        config["auth_key"],
        server_url=server_url,
    )
    return client


def get_client_usage(client: deepl.Translator) -> dict:
    usage = client.get_usage()
    return {
        "character_count": usage.character.count,
        "character_limit": usage.character.limit,
        "character_limit_reached": usage.character.limit_reached,
    }


def validate_target_language(target_lang: str) -> bool:
    valid_languages = {
        "BG",
        "CS",
        "DA",
        "DE",
        "EL",
        "EN",
        "EN-GB",
        "EN-US",
        "ES",
        "ET",
        "FI",
        "FR",
        "HU",
        "ID",
        "IT",
        "JA",
        "KO",
        "LT",
        "LV",
        "NB",
        "NL",
        "PL",
        "PT",
        "PT-BR",
        "PT-PT",
        "RO",
        "RU",
        "SK",
        "SL",
        "SV",
        "TR",
        "UK",
        "ZH",
    }
    return target_lang.upper() in valid_languages
