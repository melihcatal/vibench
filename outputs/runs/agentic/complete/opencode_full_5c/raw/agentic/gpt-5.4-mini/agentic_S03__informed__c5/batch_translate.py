from typing import List

from translation_client import translate_text_list
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_text_list,
)


def batch_translate(requests: List[TranslationRequest]) -> List[TranslationResponse]:
    texts = normalize_text_list([request.text for request in requests])
    if not requests:
        return []
    translations = translate_text_list(
        texts, requests[0].target_language, requests[0].source_language
    )
    return [
        TranslationResponse(
            translated_text=translations[index],
            source_language=request.source_language,
            target_language=request.target_language,
        )
        for index, request in enumerate(requests)
    ]
