import deepl
import os
from typing import Dict, Any, List, Optional


class DeepLTranslator:
    """Translator using DeepL API."""

    def __init__(self, auth_key: Optional[str] = None):
        self.auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable is required")

        self.translator = deepl.Translator(self.auth_key)

    def translate_text(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: Optional[str] = None,
        glossary_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Translate text using DeepL API.
        """
        try:
            result = self.translator.translate_text(
                text,
                target_lang=target_lang,
                source_lang=source_lang,
                formality=formality,
                glossary=glossary_id,
            )

            return {
                "original_text": text,
                "translated_text": result.text,
                "target_language": target_lang,
                "source_language": result.detected_source_lang
                if source_lang is None
                else source_lang,
                "provider": "deepl",
                "metadata": {
                    "detected_source_language": result.detected_source_lang
                    if source_lang is None
                    else source_lang,
                    "formality": formality,
                    "glossary_id": glossary_id,
                },
            }

        except deepl.DeepLException as e:
            return {
                "original_text": text,
                "error": str(e),
                "target_language": target_lang,
                "provider": "deepl",
            }

    def translate_batch(
        self,
        texts: List[str],
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Translate multiple texts.
        """
        results = []
        for text in texts:
            results.append(
                self.translate_text(text, target_lang, source_lang, formality)
            )
        return results

    def get_usage(self) -> Dict[str, Any]:
        """
        Get DeepL API usage information.
        """
        try:
            usage = self.translator.get_usage()

            return {
                "character_count": usage.character.count,
                "character_limit": usage.character.limit,
                "character_percentage": (
                    usage.character.count / usage.character.limit * 100
                )
                if usage.character.limit > 0
                else 0,
                "document_count": usage.document.count
                if hasattr(usage, "document")
                else 0,
                "document_limit": usage.document.limit
                if hasattr(usage, "document")
                else 0,
                "provider": "deepl",
            }
        except deepl.DeepLException as e:
            return {"error": str(e), "provider": "deepl"}

    def get_supported_languages(
        self, target_only: bool = False
    ) -> List[Dict[str, str]]:
        """
        Get list of supported languages.
        """
        try:
            if target_only:
                languages = self.translator.get_target_languages()
            else:
                languages = self.translator.get_source_languages()

            return [
                {
                    "code": lang.code,
                    "name": lang.name,
                    "supports_formality": getattr(lang, "supports_formality", False),
                }
                for lang in languages
            ]
        except deepl.DeepLException as e:
            print(f"Error getting languages: {e}")
            return []


def translate_platform_output(
    text: str, target_locale: str, source_locale: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate platform model output for another locale using DeepL.
    """
    translator = DeepLTranslator()

    deepl_target_map = {
        "en-US": "EN-US",
        "en-GB": "EN-GB",
        "es-ES": "ES",
        "es-MX": "ES",
        "fr-FR": "FR",
        "fr-CA": "FR",
        "de-DE": "DE",
        "it-IT": "IT",
        "pt-PT": "PT-PT",
        "pt-BR": "PT-BR",
        "nl-NL": "NL",
        "pl-PL": "PL",
        "ru-RU": "RU",
        "ja-JP": "JA",
        "zh-CN": "ZH",
        "zh-TW": "ZH",
    }

    deepl_source_map = {
        "en": "EN",
        "es": "ES",
        "fr": "FR",
        "de": "DE",
        "it": "IT",
        "pt": "PT",
        "nl": "NL",
        "pl": "PL",
        "ru": "RU",
        "ja": "JA",
        "zh": "ZH",
    }

    target_lang = deepl_target_map.get(target_locale, target_locale.upper())
    source_lang = None
    if source_locale:
        if "-" in source_locale:
            source_base = source_locale.split("-")[0]
            source_lang = deepl_source_map.get(source_base, source_base.upper())
        else:
            source_lang = deepl_source_map.get(source_locale, source_locale.upper())

    return translator.translate_text(text, target_lang, source_lang)


def translate_model_response(
    model_response: Dict[str, Any], target_locale: str, translate_metadata: bool = False
) -> Dict[str, Any]:
    """
    Translate a complete model response including metadata if requested.
    """
    original_text = model_response.get("text", "")

    translation_result = translate_platform_output(original_text, target_locale)

    translated_response = model_response.copy()
    translated_response["text"] = translation_result.get(
        "translated_text", original_text
    )
    translated_response["original_text"] = original_text
    translated_response["translation_metadata"] = translation_result

    if translate_metadata:
        metadata = model_response.get("metadata", {})
        translated_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, str) and len(value) < 1000:
                try:
                    trans_result = translate_platform_output(value, target_locale)
                    translated_metadata[key] = trans_result.get(
                        "translated_text", value
                    )
                except:
                    translated_metadata[key] = value
            else:
                translated_metadata[key] = value

        translated_response["metadata"] = translated_metadata

    return translated_response
