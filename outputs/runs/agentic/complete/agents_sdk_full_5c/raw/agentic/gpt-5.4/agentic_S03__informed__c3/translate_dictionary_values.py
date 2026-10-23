from __future__ import annotations

from typing import Dict, Optional

from translation_client import DEEPL_MODEL_TYPE, DeepLTranslationClient
from translation_models import TranslationRequest, normalize_mapping_values



def translate_dictionary_values(
    data: Dict[str, str],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    normalized = normalize_mapping_values(data)
    client = DeepLTranslationClient()
    items = list(normalized.items())
    response = client.translate_texts(
        [
            TranslationRequest(
                text=value,
                source_language=source_language,
                target_language=target_language,
                model_type=DEEPL_MODEL_TYPE,
            )
            for _, value in items
        ]
    )
    return {
        key: translated.text
        for (key, _), translated in zip(items, response.translations)
    }
