import os
from typing import List, Optional
from translation_client import TranslationClient
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    Formality,
)


def batch_translate(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = False,
) -> List[str]:
    client = TranslationClient()

    formality_enum = None
    if formality:
        try:
            formality_enum = Formality(formality)
        except ValueError:
            formality_enum = None

    translated_texts = client.translate_batch(
        texts=texts,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality_enum.value if formality_enum else None,
        preserve_formatting=preserve_formatting,
    )

    return translated_texts


def batch_translate_with_request(
    request: BatchTranslationRequest,
) -> BatchTranslationResponse:
    client = TranslationClient()

    translated_texts = client.translate_batch(
        texts=request.texts,
        target_lang=request.target_lang,
        source_lang=request.source_lang,
        formality=request.formality.value if request.formality else None,
        preserve_formatting=request.preserve_formatting,
    )

    total_chars = sum(len(text) for text in request.texts)

    return BatchTranslationResponse(
        translated_texts=translated_texts,
        detected_source_language=None,
        character_count=total_chars,
    )


if __name__ == "__main__":
    texts = ["Hello, world!", "How are you?", "Good morning!"]
    results = batch_translate(texts=texts, target_lang="ES", source_lang="EN")
    for i, result in enumerate(results):
        print(f"Text {i + 1}: {result}")
