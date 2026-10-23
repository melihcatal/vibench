# Translates dictionary values while preserving keys using DeepL API
from typing import Dict
from translation_client import TranslationClient
from translation_models import DictionaryTranslationRequest, TranslationResponse


def translate_dictionary_values(request: DictionaryTranslationRequest) -> Dict[str, TranslationResponse]:
    client = TranslationClient()
    source_lang, target_lang = client.normalize_languages(
        request.get("source_lang"), request["target_lang"]
    )

    texts = list(request["dictionary"].values())
    results = client.client.translate_text(
        texts,
        source_lang=source_lang,
        target_lang=target_lang
    )

    return {
        key: TranslationResponse(
            translated_text=result.text,
            detected_source_lang=result.detected_source_lang,
            model="DeepL"
        )
        for key, result in zip(request["dictionary"].keys(), results)
    }