import os
from typing import List, Optional
from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(
    texts: List[str],
    source_lang: str,
    target_lang: str,
    model: str = "google-translate-ai-v3",
    glossary_id: Optional[str] = None,
) -> List[str]:
    """Translate a list of strings while preserving order using Google Cloud Translation API."""
    client = get_translation_client()
    request = BatchTranslationRequest(
        texts=texts,
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        glossary_id=glossary_id,
    )
    response = client.batch_translate(request)
    return BatchTranslationResponse(**response).translated_texts