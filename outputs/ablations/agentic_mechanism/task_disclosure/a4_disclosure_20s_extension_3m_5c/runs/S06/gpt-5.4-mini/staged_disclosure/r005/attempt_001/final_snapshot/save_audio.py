import base64
import os
from typing import Optional, Union

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def _synthesize_speech(text: str, voice: str = "alloy", response_format: str = "mp3") -> bytes:
    api_key = os.environ["OPENAI_API_KEY"]
    response = requests.post(
        OPENAI_TTS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TTS_MODEL,
            "input": text,
            "voice": voice,
            "response_format": response_format,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.content


def save_audio(text: str, output: Optional[Union[str, os.PathLike]] = None, *, voice: str = "alloy", response_format: str = "mp3") -> Union[bytes, str]:
    audio = _synthesize_speech(text=text, voice=voice, response_format=response_format)
    if output is None:
        return audio
    path = os.fspath(output)
    with open(path, "wb") as f:
        f.write(audio)
    return path


def save_audio_base64(text: str, *, voice: str = "alloy", response_format: str = "mp3") -> str:
    audio = _synthesize_speech(text=text, voice=voice, response_format=response_format)
    return base64.b64encode(audio).decode("utf-8")
