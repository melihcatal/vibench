from __future__ import annotations

from typing import Iterable, List

from google.cloud import translate_v3 as translate

from speech_models import TranscriptWord


def translate_transcript(segments: Iterable[TranscriptWord], target_language: str = "en") -> List[str]:
    client = translate.TranslationServiceClient()
    parent = "projects/placeholder/locations/global"
    translated: List[str] = []
    for segment in segments:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [segment.text],
                "mime_type": "text/plain",
                "target_language_code": target_language,
            }
        )
        translated.append(response.translations[0].translated_text if response.translations else segment.text)
    return translated
