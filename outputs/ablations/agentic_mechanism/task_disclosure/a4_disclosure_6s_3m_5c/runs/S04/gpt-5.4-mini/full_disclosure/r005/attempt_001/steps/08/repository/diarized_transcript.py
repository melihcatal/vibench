import os
from typing import Any, Dict, Optional

import requests


OPENAI_TRANSCRIPTION_URL = "https://api.openai.com/v1/audio/transcriptions"


def request_speaker_diarization(audio_file_path: str, model: str = "gpt-4o-transcribe", language: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    with open(audio_file_path, "rb") as audio_file:
        files = {"file": audio_file}
        data = {"model": model, "response_format": "verbose_json", "timestamp_granularities[]": ["segment"], "diarize": "true"}
        if language:
            data["language"] = language
        response = requests.post(
            OPENAI_TRANSCRIPTION_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            files=files,
            data=data,
            timeout=300,
        )
    response.raise_for_status()
    return response.json()
