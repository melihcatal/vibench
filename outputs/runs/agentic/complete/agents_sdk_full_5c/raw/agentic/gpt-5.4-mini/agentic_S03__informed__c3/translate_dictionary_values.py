from __future__ import annotations

from translation_client import TranslationClient
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse


DEEPL_PROVIDER = "DeepL API"


def translate_dictionary_values(values: dict[str, str], source_language: str, target_language: str) -> DictionaryTranslationResponse:
    client = TranslationClient()
    translated_values = client.translate_dictionary_values(
        DictionaryTranslationRequest(
            values=values,
            source_language=source_language,
            target_language=target_language,
        )
    )
    return DictionaryTranslationResponse(
        translated_values=translated_values,
        provider=DEEPL_PROVIDER,
        metadata={"service": "deepl", "keys_preserved": True},
    )
