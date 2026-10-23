from typing import Any, Dict

import requests

from speech_client import load_speech_config


AZURE_DIARIZATION_ENDPOINT = "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions"


def diarized_transcript(audio_url: str) -> Dict[str, Any]:
    cfg = load_speech_config()
    headers = {
        "Ocp-Apim-Subscription-Key": cfg.api_key,
        "Content-Type": "application/json",
    }
    body = {
        "contentUrls": [audio_url],
        "locale": cfg.language,
        "properties": {
            "diarizationEnabled": True,
            "wordLevelTimestampsEnabled": True,
        },
        "displayName": "diarized-meeting",
    }
    response = requests.post(AZURE_DIARIZATION_ENDPOINT, json=body, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
