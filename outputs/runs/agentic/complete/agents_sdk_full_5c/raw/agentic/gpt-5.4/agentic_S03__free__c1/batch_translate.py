from __future__ import annotations

from typing import List, Optional

from translation_client import get_google_parent, get_translate_client
from translation_models import BatchTranslationRequest, BatchTranslationResult, normalize_translation_items


TRANSLATION_MODEL = "general/nmt"


def batch_translate(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> BatchTranslationResult:
    client = get_translate_client()
    parent = get_google_parent(project_id=project_id, location=location)
    request = BatchTranslationRequest(
        texts=texts,
        source_language=source_language,
        target_language=target_language,
        content_type="text/plain",
    )
    response = client.translate_text(
        request={
            "parent": parent,
            **request.as_google_translate_payload(),
            "model": f"projects/{parent.split('/')[1]}/locations/{parent.split('/')[-1]}/models/{TRANSLATION_MODEL}",
        }
    )
    normalized = normalize_translation_items(
        {
            "translated_text": item.translated_text,
            "detected_language_code": getattr(item, "detected_language_code", None),
            "index": index,
        }
        for index, item in enumerate(response.translations)
    )
    return BatchTranslationResult(translations=normalized, metadata={"count": len(normalized)})
