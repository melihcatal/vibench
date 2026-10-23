from __future__ import annotations

import base64
import os

import requests

from translation_client import GOOGLE_CLOUD_TTS_ENDPOINT


def localized_audio_preview(
    text: str, language_code: str, voice_name: str | None = None
) -> bytes:
    response = requests.post(
        GOOGLE_CLOUD_TTS_ENDPOINT,
        params={"key": os.environ["GOOGLE_CLOUD_API_KEY"]},
        json={
            "input": {"text": text},
            "voice": {
                "languageCode": language_code,
                "name": voice_name or f"{language_code}-Standard-A",
            },
            "audioConfig": {"audioEncoding": "MP3"},
        },
        timeout=30,
    )
    response.raise_for_status()
    return base64.b64decode(response.json()["audioContent"])
