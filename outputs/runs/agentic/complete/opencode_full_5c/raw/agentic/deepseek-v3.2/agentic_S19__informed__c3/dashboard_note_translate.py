import os
from typing import Dict, Any
import deepl


def translate_dashboard_note(text: str, target_language: str = "DE") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        raise Exception(f"DeepL translation failed: {str(e)}")


def translate_metric_descriptions(
    descriptions: Dict[str, str], target_language: str = "FR"
) -> Dict[str, str]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    translated = {}
    for metric_name, description in descriptions.items():
        try:
            result = translator.translate_text(description, target_lang=target_language)
            translated[metric_name] = result.text
        except deepl.DeepLException as e:
            translated[metric_name] = f"[Translation failed: {str(e)}]"

    return translated


def get_supported_languages() -> Dict[str, str]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    languages = {}
    try:
        source_langs = translator.get_source_languages()
        target_langs = translator.get_target_languages()

        for lang in source_langs:
            languages[lang.code] = {
                "name": lang.name,
                "supports_formality": getattr(lang, "supports_formality", False),
                "type": "source",
            }

        for lang in target_langs:
            if lang.code not in languages:
                languages[lang.code] = {
                    "name": lang.name,
                    "supports_formality": getattr(lang, "supports_formality", False),
                    "type": "target",
                }
            else:
                languages[lang.code]["type"] = "both"

        return languages
    except deepl.DeepLException as e:
        return {"error": str(e)}


def translate_with_context(
    text: str, target_language: str, context: str = "monitoring dashboard"
) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(
            text, target_lang=target_language, context=context
        )
        return result.text
    except deepl.DeepLException as e:
        raise Exception(f"DeepL translation failed: {str(e)}")
