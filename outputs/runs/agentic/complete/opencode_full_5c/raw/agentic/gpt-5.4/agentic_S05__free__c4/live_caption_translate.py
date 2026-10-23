from __future__ import annotations

from typing import Iterable, List

from google.cloud import translate_v2 as translate

from speech_models import CaptionSegment, normalize_transcript_text


def translate_live_captions(
    segments: Iterable[CaptionSegment], target_language: str
) -> List[str]:
    client = translate.Client()
    translated: List[str] = []
    for segment in segments:
        text = normalize_transcript_text(segment.text)
        if not text:
            continue
        response = client.translate(
            text, target_language=target_language, format_="text"
        )
        translated.append(response["translatedText"])
    return translated
