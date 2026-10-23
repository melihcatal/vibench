from typing import List
from translation_client import deepl_translator
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    if not deepl_translator:
        raise ValueError(
            "DeepL translator not initialized. Please set DEEPL_AUTH_KEY environment variable."
        )

    results = deepl_translator.translate_text(
        request.texts, target_lang=request.target_lang, source_lang=request.source_lang
    )
    translated_texts = [res.text for res in results]

    # DeepL may return a single detected source language for a batch, or individual ones
    source_lang = None
    if results and hasattr(
        results[0], "detected_source_lang"
    ):  # Check if individual source lang is present
        # If all source languages are the same, we can return a single source_lang
        if all(
            res.detected_source_lang == results[0].detected_source_lang
            for res in results
        ):
            source_lang = results[0].detected_source_lang
    elif hasattr(
        results, "detected_source_lang"
    ):  # Check if batch result has a single detected source lang
        source_lang = results.detected_source_lang

    return BatchTranslationResponse(
        translated_texts=translated_texts,
        source_lang=source_lang,
        target_lang=request.target_lang,
    )
