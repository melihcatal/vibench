import base64
import mimetypes
import os
from typing import Any, Dict, Optional

import requests


OPENAI_TRANSCRIPTION_URL = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_TRANSCRIPTION_MODEL = "gpt-4o-transcribe"


def submit_transcription(audio_path: str, model: str = OPENAI_TRANSCRIPTION_MODEL, language: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    mime_type, _ = mimetypes.guess_type(audio_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    with open(audio_path, "rb") as audio_file:
        files = {
            "file": (os.path.basename(audio_path), audio_file, mime_type),
        }
        data = {"model": model}
        if language:
            data["language"] = language

        response = requests.post(
            OPENAI_TRANSCRIPTION_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            files=files,
            data=data,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
