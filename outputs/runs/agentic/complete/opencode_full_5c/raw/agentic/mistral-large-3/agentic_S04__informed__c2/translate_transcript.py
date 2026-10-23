import os
from typing import List, Dict, Any
from google.cloud import translate_v2 as translate


def translate_transcript(
    segments: List[Dict[str, Any]], target_language: str
) -> List[Dict[str, Any]]:
    client = translate.Client()
    translated_segments = []
    for segment in segments:
        result = client.translate(segment["text"], target_language=target_language)
        translated_segments.append(
            {**segment, "translated_text": result["translatedText"]}
        )
    return translated_segments
