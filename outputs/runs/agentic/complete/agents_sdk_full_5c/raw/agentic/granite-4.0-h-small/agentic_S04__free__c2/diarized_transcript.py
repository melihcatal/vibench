import json
import os
from typing import Any

# Assume the service uses Azure Cognitive Services Batch Speech-to-Text
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, AudioDataStream, SpeechSynthesizer

# Load endpoint and key from environment (these should be set in your runtime environment)
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SERVICE_REGION = os.getenv("AZURE_SPEECH_REGION")

def submit_diarized_transcription(audio_path: str, callback_url: str = None, diarization: bool = True) -> Any:
    """Submit a batch transcription request with speaker diarization enabled.

    Returns the JSON response containing the job ID.
    """
    speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
    params = {
        "contentUrls": [audio_path],
        "properties": {
            "diarization": diarization,
            "timestamps": True,
            "callbackUrl": callback_url,
        },
    }
    import requests
    url = f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speech/batch/v1"
    headers = {
        "Authorization": f"Bearer {SPEECH_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=params, headers=headers)
    response.raise_for_status()
    return response.json()

# Export only the submit helper needed by later steps
__all__ = ["submit_diarized_transcription"]
