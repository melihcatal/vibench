import os
from typing import Any, Dict

import requests

from speech_client import load_speech_config
from speech_models import TranscriptionSubmitRequest


AZURE_SPEECH_ENDPOINT = "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions"


def submit_transcription(audio_url: str) -> Dict[str, Any]:
    cfg = load_speech_config()
    payload = TranscriptionSubmitRequest(audio_url=audio_url, language=cfg.language, display_name="batch-transcription").__dict__
    headers = {
        "Ocp-Apim-Subscription-Key": cfg.api_key,
        "Content-Type": "application/json",
    }
    body = {
        "contentUrls": [payload["audio_url"]],
        "locale": payload["language"],
        "displayName": payload["display_name"],
    }
    response = requests.post(AZURE_SPEECH_ENDPOINT, json=body, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
