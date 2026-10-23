from typing import List
from translation_client import get_deepl_translator
from translation_models import TranslationRequest, TranslationResponse


def batch_translate_texts(request: TranslationRequest) -> TranslationResponse:
    if not isinstance(request.text, list):
        raise ValueError("Expected a list of strings for batch translation.")

    translator = get_deepl_translator()
    results = translator.translate_text(
        request.text, target_lang=request.target_lang, source_lang=request.source_lang
    )
    translated_texts = [result.text for result in results]
    detected_source_langs = [result.detected_source_lang for result in results]
    # For simplicity, we'll return the first detected source language if multiple are detected
    detected_source_lang = detected_source_langs[0] if detected_source_langs else None

    return TranslationResponse(
        translated_text=translated_texts, detected_source_lang=detected_source_lang
    )
