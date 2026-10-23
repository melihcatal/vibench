import os
import requests

# Example: Google Cloud Text-to-Speech (Text-to-Speech later-step)\n# Provider identification via endpoint hostname and auth header

# ------------------------------------------------------------------\n# Configuration – set required env vars before running\n# ------------------------------------------------------------------\nGOOGLE_APPLICATION_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)
TTS_ENDPOINT = os.getenv(
    "GOOGLE_TTS_ENDPOINT",
    "https://texttospeech.googleapis.com/v1/text:synthesize"
)
API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError(
        "Set GOOGLE_APPLICATION_CREDENTIALS to a valid service account JSON file."
    )
if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY for Text‑to‑Speech.")


def generate_spoken_brief(text: str, language_code: str = "en-US") -> bytes:
    """Synthesizes the provided text into an audio file (WAV) using GCP TTS."""
    payload = {
        "input": {
            "text": text
        },
        "voice": {
            "languageCode": language_code,
            "name": "en-US-Wavenet-D",
            "ssmlGender": "FEMALE"
        },
        "audioConfig": {
            "audioEncoding": "LINEAR16"
        }
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(TTS_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    # Audio is returned as binary content (BASE64 encoded in protobuf, but the API returns raw audio)
    audio_content = response.content
    return audio_content
