from __future__ import annotations

from typing import List, Optional, Sequence

from translation_client import DEEPL_MODEL_TYPE, DeepLTranslationClient
from translation_models import TranslationRequest, normalize_texts



def batch_translate(
    texts: Sequence[str],
    target_language: str,
    source_language: Optional[str] = None,
    formality: Optional[str] = None,
) -> List[str]:
    normalized = normalize_texts(texts)
    client = DeepLTranslationClient()
    requests = [
        TranslationRequest(
            text=text,
            source_language=source_language,
            target_language=target_language,
            formality=formality,
            model_type=DEEPL_MODEL_TYPE,
        )
        for text in normalized
    ]
    response = client.translate_texts(requests)
    return [item.text for item in response.translations]
