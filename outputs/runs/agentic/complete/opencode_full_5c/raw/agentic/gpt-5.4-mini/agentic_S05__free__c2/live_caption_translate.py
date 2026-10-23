import os
from typing import Iterable, List

from google.cloud import translate_v3

from speech_models import normalize_chunks


def translate_live_captions(chunks: Iterable[str], target_language: str) -> List[str]:
    client = translate_v3.TranslationServiceClient()
    parent = client.common_location_path(
        os.getenv("GOOGLE_CLOUD_PROJECT", "project"),
        os.getenv("GOOGLE_CLOUD_LOCATION", "global"),
    )
    texts = normalize_chunks(chunks)
    if not texts:
        return []
    response = client.translate_text(
        parent=parent,
        contents=texts,
        mime_type="text/plain",
        target_language_code=target_language,
    )
    return [item.translated_text for item in response.translations]
