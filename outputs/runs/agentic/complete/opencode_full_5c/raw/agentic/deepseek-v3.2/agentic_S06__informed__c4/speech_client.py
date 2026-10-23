import os
from typing import Optional
from google.cloud import texttospeech


def get_tts_client() -> texttospeech.TextToSpeechClient:
    """Get Google Cloud Text-to-Speech client with configuration."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        return texttospeech.TextToSpeechClient.from_service_account_json(
            credentials_path
        )
    else:
        return texttospeech.TextToSpeechClient()


def get_tts_client_with_project(
    project_id: Optional[str] = None,
) -> texttospeech.TextToSpeechClient:
    """Get Google Cloud Text-to-Speech client with specific project."""
    client = get_tts_client()

    if project_id:
        client.project = project_id

    return client


def validate_tts_config() -> bool:
    """Validate TTS configuration and credentials."""
    try:
        client = get_tts_client()
        client.list_voices(language_code="en-US")
        return True
    except Exception as e:
        print(f"TTS configuration validation failed: {e}")
        return False
