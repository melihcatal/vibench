from typing import List

from translation_client import (
    get_source_language,
    get_target_language,
    get_translation_client,
)
from translation_models import TranslationResponse, normalize_text_list


def batch_translate(
    texts: List[str], source_language: str, target_language: str
) -> List[TranslationResponse]:
    client = get_translation_client()
    normalized = normalize_text_list(texts)
    results = client.translate_text(
        normalized,
        source_lang=get_source_language(source_language),
        target_lang=get_target_language(target_language),
    )
    return [
        TranslationResponse(
            translated_text=item.text,
            detected_source_language=getattr(item, "detected_source_lang", None),
            provider="deepl",
        )
        for item in results
    ]
