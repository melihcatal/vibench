import os
from google.cloud import translate_v2 as translate
from speech_models import TranscriptionUtterance


def translate_transcript_segments(
    segments: list[TranscriptionUtterance], target_language: str = "es"
) -> list[str]:
    """
    Translates transcript segments using Google Cloud Translate.
    """
    os.environ.setdefault(
        "GOOGLE_APPLICATION_CREDENTIALS",
        os.path.expanduser("~/.config/gcloud/application_default_credentials.json"),
    )
    translate_client = translate.Client()

    translated_segments = []
    for segment in segments:
        result = translate_client.translate(
            segment.text, target_language=target_language
        )
        translated_segments.append(result["translatedText"])

    return translated_segments
