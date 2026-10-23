from __future__ import annotations

import os
import sys
import typing

from translation_client import load_auth_token, normalize_request, get_provider_config
from translation_models import DictionaryValuesRequest, DictionaryValuesResponse

# Map of provider name to entrypoint function (stubbed here)
PROVIDERS = {
    "deepl": "translate_dict_deepl",
    "google": "translate_dict_google",
    "azure": "translate_dict_azure",
    "amazon": "translate_dict_amazon",
    "alibaba": "translate_dict_alibaba",
}


def translate_dictionary_values(
    dictionary: dict[str, str],
    source_lang: str,
    target_lang: str,
    provider: str = "deepl",
) -> DictionaryValuesResponse:
    """
    Translate the values of a dictionary while preserving keys.

    Args:
        dictionary: Mapping where values are strings to translate.
        source_lang: ISO 639-1 source language code.
        target_lang: ISO 639-1 target language code.
        provider: Provider identifier.

    Returns:
        DictionaryValuesResponse with translated dictionary.
    """
    if provider not in PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {provider}. Choose from {list(PROVIDERS)}"
        )

    auth_token = load_auth_token(provider)
    cfg = get_provider_config(provider)
    # Normalize the generic request to provider's expected shape
    payload = normalize_request(
        {
            "dictionary": dictionary,
            "source_lang": source_lang,
            "target_lang": target_lang,
        },
        provider,
    )
    # Call concrete provider stub (handles iteration and translation)
    result = globals()[PROVIDERS[provider]](auth_token, payload)
    return result


# --------------------------------------------------------------------
# Concrete provider stubs (replace with real SDK calls in production)
# --------------------------------------------------------------------
def translate_dict_deepl(auth: str, payload: dict) -> DictionaryValuesResponse:
    # Assume payload['dictionary'] is a dict; translate each value
    translated = {
        k: f"[DeePL] '{v}' → {payload['target_lang']}"
        for k, v in payload["dictionary"].items()
    }
    return DictionaryValuesResponse(dictionary=translated)


def translate_dict_google(auth: str, payload: dict) -> DictionaryValuesResponse:
    translated = {
        k: f"[Google] '{v}' → {payload['target_lang']}"
        for k, v in payload["dictionary"].items()
    }
    return DictionaryValuesResponse(dictionary=translated)


def translate_dict_azure(auth: str, payload: dict) -> DictionaryValuesResponse:
    translated = {
        k: f"[Azure] '{v}' → {payload['target_lang']}"
        for k, v in payload["dictionary"].items()
    }
    return DictionaryValuesResponse(dictionary=translated)


def translate_dict_amazon(auth: str, payload: dict) -> DictionaryValuesResponse:
    translated = {
        k: f"[Amazon] '{v}' → {payload['target_lang']}"
        for k, v in payload["dictionary"].items()
    }
    return DictionaryValuesResponse(dictionary=translated)


def translate_dict_alibaba(auth: str, payload: dict) -> DictionaryValuesResponse:
    translated = {
        k: f"[Alibaba] '{v}' → {payload['target_lang']}"
        for k, v in payload["dictionary"].items()
    }
    return DictionaryValuesResponse(dictionary=translated)


# --------------------------------------------------------------------
# CLI helper for testing
# --------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            f'Usage: {sys.argv[0]} "key1:value1,key2:value2" <source_lang> <target_lang> <provider>\nProvider choices: {", ".join(PROVIDERS)}'
        )
        sys.exit(1)
    _, raw_dict, src, tgt, prov = sys.argv
    # Parse key:value pairs into a dict
    raw_pairs = raw_dict.split(",")
    dictionary = {pair.split(":")[0]: pair.split(":")[1] for pair in raw_pairs}
    result = translate_dictionary_values(dictionary, src, tgt, prov)
    print(result["dictionary"])
