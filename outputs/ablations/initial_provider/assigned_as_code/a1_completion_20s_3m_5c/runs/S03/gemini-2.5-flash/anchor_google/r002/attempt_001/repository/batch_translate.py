from typing import List
from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(payload: BatchTranslationRequest, config: dict) -> BatchTranslationResponse:
    client = TranslationClient(project_id=config["project_id"], location=config.get("location", "global"))
    translated_texts = client.translate_text(
        texts=payload.texts,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
    return BatchTranslationResponse(
        translated_texts=translated_texts,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
