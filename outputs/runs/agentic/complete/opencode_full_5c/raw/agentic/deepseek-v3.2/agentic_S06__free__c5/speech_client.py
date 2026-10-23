import os
from google.cloud import texttospeech
from google.oauth2 import service_account


def get_tts_client():
    """Provide Google Cloud TTS client with configuration."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        client = texttospeech.TextToSpeechClient(credentials=credentials)
    else:
        client = texttospeech.TextToSpeechClient()

    return client


def get_default_config():
    """Get default TTS configuration."""
    return {
        "default_language": "en-US",
        "default_voice": "en-US-Standard-A",
        "default_encoding": "MP3",
        "default_sample_rate": 24000,
    }


def validate_audio_config(audio_config):
    """Validate audio configuration parameters."""
    valid_encodings = ["MP3", "LINEAR16", "OGG_OPUS", "MULAW", "ALAW"]

    if audio_config.get("audio_encoding") not in valid_encodings:
        audio_config["audio_encoding"] = "MP3"

    if "speaking_rate" in audio_config:
        rate = audio_config["speaking_rate"]
        if rate < 0.25 or rate > 4.0:
            audio_config["speaking_rate"] = 1.0

    if "pitch" in audio_config:
        pitch = audio_config["pitch"]
        if pitch < -20.0 or pitch > 20.0:
            audio_config["pitch"] = 0.0

    return audio_config
