import os
import json
import requests
from typing import List, Dict
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load credentials
API_KEY = os.getenv("IBM_STT_APIKEY")
SERVICE_URL = os.getenv("IBM_STT_URL")
assert API_KEY and SERVICE_URL, "Set IBM_STT_APIKEY and IBM_STT_URL"

authenticator = IAMAuthenticator(API_KEY)
client = SpeechToTextV1(authenticator=authenticator)
client.set_service_url(SERVICE_URL)

CHANNELS = ["narrowband", "broadband"]


def transcribe_audio_bytes(
    audio_bytes: bytes, model: str = "en-US_NarrowbandModel"
) -> List[Dict]:
    """Transcribe raw audio bytes using Watson Speech-to-Text and return list of transcript dicts."""
    result = client.recognize(
        audio=audio_bytes, model=model, content_type="audio/wav"
    ).get_result()
    return result["results"]


def transcribe_local_file(
    file_path: str, model: str = "en-US_NarrowbandModel"
) -> List[Dict]:
    """Upload a local WAV file for transcription."""
    with open(file_path, "rb") as audio_file:
        result = client.recognize(
            audio_file, model=model, content_type="audio/wav"
        ).get_result()
    return result["results"]


# Helper to list available models (optional)
def list_models() -> List[str]:
    models = client.list_models().get_result()["models"]
    return [m["name"] for m in models]
