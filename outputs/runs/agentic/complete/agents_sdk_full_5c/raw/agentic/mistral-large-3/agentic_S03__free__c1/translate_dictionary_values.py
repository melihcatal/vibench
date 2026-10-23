import os
from typing import Dict, List, Optional
from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def translate_dictionary_values(
    dictionary: Dict[str, str],
    source_lang: str,
    target_lang: str,
    model: str = "google-translate-ai-v3",
    glossary_id: Optional[str] = None,
) -> Dict[str, str]:
    """Translate dictionary values while preserving keys using Google Cloud Translation API."""
    texts = list(dictionary.values())
    client = get_translation_client()
    request = BatchTranslationRequest(
        texts=texts,
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        glossary_id=glossary_id,
    )
    response = client.batch_translate(request)
    translated_texts = BatchTranslationResponse(**response).translated_texts

    return {key: translated_texts[idx] for idx, key in enumerate(dictionary.keys())}