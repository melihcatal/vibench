from google.cloud import translate_v2 as translate
from typing import List, Dict


def translate_transcript(
    transcript_segments: List[Dict[str, str]], target_language: str = "es"
) -> List[Dict[str, str]]:
    """Translate completed transcript segments using Google Cloud Translation API."""
    client = translate.Client()

    translated_segments = []
    for segment in transcript_segments:
        text = segment["text"]
        result = client.translate(text, target_language=target_language)

        translated_segments.append(
            {
                "original_text": text,
                "translated_text": result["translatedText"],
                "language": result["detectedSourceLanguage"],
            }
        )

    return translated_segments
