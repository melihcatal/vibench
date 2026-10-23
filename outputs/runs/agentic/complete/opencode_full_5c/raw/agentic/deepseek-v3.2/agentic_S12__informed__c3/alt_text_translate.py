import os
from typing import List, Dict, Any
import deepl


def translate_alt_text(
    alt_text: str, target_language: str = "DE", auth_key: str = None
) -> str:
    if auth_key is None:
        auth_key = os.environ.get("DEEPL_AUTH_KEY")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(alt_text, target_lang=target_language)

    return result.text


def translate_image_descriptions(
    descriptions: List[Dict[str, Any]],
    target_language: str = "DE",
    auth_key: str = None,
) -> List[Dict[str, Any]]:
    if auth_key is None:
        auth_key = os.environ.get("DEEPL_AUTH_KEY")

    translator = deepl.Translator(auth_key)

    translated_descriptions = []
    for desc in descriptions:
        original_text = desc.get("description", "")
        if original_text:
            translated_text = translator.translate_text(
                original_text, target_lang=target_language
            ).text

            translated_desc = desc.copy()
            translated_desc["description"] = translated_text
            translated_desc["original_description"] = original_text
            translated_desc["target_language"] = target_language
            translated_descriptions.append(translated_desc)
        else:
            translated_descriptions.append(desc)

    return translated_descriptions


def translate_multiple_languages(
    alt_text: str, target_languages: List[str], auth_key: str = None
) -> Dict[str, str]:
    if auth_key is None:
        auth_key = os.environ.get("DEEPL_AUTH_KEY")

    translator = deepl.Translator(auth_key)

    translations = {}
    for lang in target_languages:
        result = translator.translate_text(alt_text, target_lang=lang)
        translations[lang] = result.text

    return translations


def get_supported_languages(auth_key: str = None) -> List[Dict[str, str]]:
    if auth_key is None:
        auth_key = os.environ.get("DEEPL_AUTH_KEY")

    translator = deepl.Translator(auth_key)

    source_languages = translator.get_source_languages()
    target_languages = translator.get_target_languages()

    return {
        "source_languages": [
            {"code": lang.code, "name": lang.name} for lang in source_languages
        ],
        "target_languages": [
            {"code": lang.code, "name": lang.name} for lang in target_languages
        ],
    }
