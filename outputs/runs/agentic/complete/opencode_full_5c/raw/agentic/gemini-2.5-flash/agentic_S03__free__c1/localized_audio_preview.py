import os
from translation_client import TranslationClient
from translation_models import AudioPreviewRequest

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_localized_audio_preview(request: AudioPreviewRequest) -> bytes:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = TranslationClient(project_id=PROJECT_ID)
    audio_content = client.synthesize_speech(
        request.text, request.language_code, request.voice_name, request.ssml_gender
    )
    return audio_content
