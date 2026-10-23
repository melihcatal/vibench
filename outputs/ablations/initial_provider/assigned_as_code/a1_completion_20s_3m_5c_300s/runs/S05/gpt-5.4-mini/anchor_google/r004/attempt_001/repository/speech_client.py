import os
from google.cloud import speech


def load_speech_settings(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.getenv("GOOGLE_CLOUD_PROJECT"),
        "language_code": config.get("language_code") or os.getenv("SPEECH_LANGUAGE_CODE", "en-US"),
        "enable_punctuation": bool(config.get("enable_punctuation", True)),
    }


def create_speech_client(config=None):
    settings = load_speech_settings(config)
    client = speech.SpeechClient()
    return client, settings
