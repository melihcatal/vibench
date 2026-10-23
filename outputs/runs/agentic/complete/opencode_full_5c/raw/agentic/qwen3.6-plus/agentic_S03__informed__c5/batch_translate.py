import os
from deepl import Translator
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    TranslationRequest,
    TranslationResponse,
)
from translation_client import get_deepl_client, normalize_language_code


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = get_deepl_client()
    source_lang = normalize_language_code(request.source_lang)
    target_lang = normalize_language_code(request.target_lang)

    results = client.translate_text(
        request.texts,
        source_lang=source_lang if source_lang else None,
        target_lang=target_lang,
    )

    translations = []
    for idx, result in enumerate(results):
        translations.append(
            TranslationResponse(
                translated_text=result.text,
                source_lang=result.detected_source_lang or request.source_lang,
                target_lang=target_lang,
                confidence=1.0,
            )
        )

    return BatchTranslationResponse(
        translations=translations,
        source_lang=request.source_lang,
        target_lang=target_lang,
    )


if __name__ == "__main__":
    req = BatchTranslationRequest(
        texts=["Hello world", "Good morning", "Thank you"],
        source_lang="en",
        target_lang="es",
    )
    resp = batch_translate(req)
    for t in resp.translations:
        print(t.translated_text)
