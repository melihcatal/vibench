import os
import requests

DEEPL_API_KEY_ENV = "DEEPL_API_KEY"
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def welcome_translate(text, target_locale):
    api_key = os.environ[DEEPL_API_KEY_ENV]

    target_lang = _map_locale_to_deepl_lang(target_locale)

    params = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_lang,
    }

    response = requests.post(DEEPL_API_URL, data=params, timeout=30)
    response.raise_for_status()

    result = response.json()
    translations = result.get("translations", [])
    if translations:
        return translations[0].get("text", text)
    return text


def _map_locale_to_deepl_lang(locale):
    locale_map = {
        "en": "EN",
        "en-US": "EN-US",
        "en-GB": "EN-GB",
        "es": "ES",
        "fr": "FR",
        "de": "DE",
        "it": "IT",
        "pt": "PT",
        "pt-BR": "PT-BR",
        "nl": "NL",
        "pl": "PL",
        "ru": "RU",
        "ja": "JA",
        "zh": "ZH",
        "zh-CN": "ZH",
        "ko": "KO",
    }
    return locale_map.get(locale, locale.split("-")[0].upper())
