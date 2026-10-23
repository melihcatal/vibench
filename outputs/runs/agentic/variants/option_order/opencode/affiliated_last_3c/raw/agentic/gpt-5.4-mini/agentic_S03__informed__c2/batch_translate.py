from translation_client import create_translation_client
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResult,
    normalize_text_list,
)


def batch_translate(texts, source_language=None, target_language="en"):
    request = BatchTranslationRequest(
        texts=normalize_text_list(texts),
        source_language=source_language,
        target_language=target_language,
    )
    client = create_translation_client()
    translated = client.translate_text(
        request.texts,
        source_lang=request.source_language,
        target_lang=request.target_language,
    )
    return BatchTranslationResult(
        translated_texts=[item.text for item in translated],
        metadata={"provider": "deepl"},
    )
