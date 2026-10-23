import os
from typing import Optional

from openai import OpenAI


def synthesize_ssml(ssml: str, voice: str = "alloy", model: str = "gpt-4o-mini-tts", speed: Optional[float] = None) -> bytes:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    params = {"model": model, "voice": voice, "input": ssml, "format": "mp3"}
    if speed is not None:
        params["speed"] = speed
    response = client.audio.speech.create(**params)
    return response.read()
