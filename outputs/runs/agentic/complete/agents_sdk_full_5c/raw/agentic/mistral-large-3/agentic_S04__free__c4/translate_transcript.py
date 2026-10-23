from google.cloud import translate_v3 as translate
from speech_models import TranscriptionResult

def translate_transcript(transcript: str, target_language: str = "es") -> str:
    """Translate completed transcript segments using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{client.project}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[transcript],
        mime_type="text/plain",
        target_language_code=target_language,
        model="nmt",
    )

    return response.translations[0].translated_text