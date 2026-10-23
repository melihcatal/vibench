import os
from google.cloud import texttospeech

def get_tts_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()

def get_tts_parent() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")
    return f"projects/{project_id}/locations/global"
