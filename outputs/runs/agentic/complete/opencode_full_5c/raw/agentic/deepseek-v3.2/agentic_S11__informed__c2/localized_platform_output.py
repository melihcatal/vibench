import os
import deepl
from typing import Dict, Any, Optional


def translate_with_deepl(
    text: str, target_lang: str = "DE", source_lang: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate platform model output using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError(
            "DeepL authentication key must be set in DEEPL_AUTH_KEY environment variable"
        )

    try:
        translator = deepl.Translator(auth_key)

        result = translator.translate_text(
            text, target_lang=target_lang, source_lang=source_lang
        )

        return {
            "original_text": text,
            "translated_text": result.text,
            "target_language": target_lang,
            "source_language": result.detected_source_lang
            if source_lang is None
            else source_lang,
            "provider": "DeepL",
        }

    except deepl.DeepLException as e:
        return {
            "original_text": text,
            "translated_text": "",
            "error": f"DeepL translation error: {str(e)}",
            "target_language": target_lang,
            "provider": "DeepL",
        }


def translate_for_locale(
    text: str, locale: str, preserve_formatting: bool = True
) -> Dict[str, Any]:
    """
    Translate text for a specific locale/language.
    Supports common locale codes.
    """
    locale_to_deepl = {
        "en-US": "EN-US",
        "en-GB": "EN-GB",
        "de-DE": "DE",
        "fr-FR": "FR",
        "es-ES": "ES",
        "it-IT": "IT",
        "nl-NL": "NL",
        "pl-PL": "PL",
        "pt-PT": "PT-PT",
        "pt-BR": "PT-BR",
        "ru-RU": "RU",
        "ja-JP": "JA",
        "zh-CN": "ZH",
        "ko-KR": "KO",
    }

    target_lang = locale_to_deepl.get(locale, "EN-US")

    if "-" in target_lang:
        source_lang = None
    else:
        source_lang = "EN"

    result = translate_with_deepl(
        text=text, target_lang=target_lang, source_lang=source_lang
    )

    result["locale"] = locale
    result["preserve_formatting"] = preserve_formatting

    return result


def batch_translate(
    texts: list, target_lang: str = "DE", source_lang: Optional[str] = None
) -> list:
    """
    Translate multiple texts in batch.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError(
            "DeepL authentication key must be set in DEEPL_AUTH_KEY environment variable"
        )

    try:
        translator = deepl.Translator(auth_key)

        results = translator.translate_text(
            texts, target_lang=target_lang, source_lang=source_lang
        )

        translations = []
        for original, translated in zip(texts, results):
            translations.append(
                {
                    "original_text": original,
                    "translated_text": translated.text,
                    "target_language": target_lang,
                    "source_language": translated.detected_source_lang
                    if source_lang is None
                    else source_lang,
                }
            )

        return translations

    except deepl.DeepLException as e:
        return [
            {
                "original_text": text,
                "translated_text": "",
                "error": f"DeepL batch translation error: {str(e)}",
            }
            for text in texts
        ]
