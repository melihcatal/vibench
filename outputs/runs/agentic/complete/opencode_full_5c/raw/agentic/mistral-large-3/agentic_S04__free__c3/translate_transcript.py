from google.cloud import translate_v2 as translate
from typing import List, Dict
import os


def translate_transcript(
    transcript_segments: List[Dict[str, str]], target_language: str = "es"
) -> List[Dict[str, str]]:
    """Translate completed transcript segments using Google Cloud Translation API."""
    client = translate.Client()
    translated_segments = []

    for segment in transcript_segments:
        text = segment.get("text", "")
        if text:
            result = client.translate(text, target_language=target_language)
            translated_segments.append(
                {
                    "original_text": text,
                    "translated_text": result["translatedText"],
                    "speaker": segment.get("speaker"),
                    "start_time": segment.get("start_time"),
                    "end_time": segment.get("end_time"),
                }
            )

    return translated_segments
