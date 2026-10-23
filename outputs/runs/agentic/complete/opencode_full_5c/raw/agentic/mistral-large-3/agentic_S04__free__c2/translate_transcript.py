from google.cloud import translate_v2 as translate
from speech_models import TranscriptionResult
import os


def translate_transcript(transcript: TranscriptionResult, target_language: str) -> dict:
    client = translate.Client()

    translations = {}
    for segment in transcript.segments:
        result = client.translate(
            segment.text,
            target_language=target_language,
            source_language=transcript.language_code.split("-")[0],
        )
        translations[segment.text] = {
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
        }

    return translations
