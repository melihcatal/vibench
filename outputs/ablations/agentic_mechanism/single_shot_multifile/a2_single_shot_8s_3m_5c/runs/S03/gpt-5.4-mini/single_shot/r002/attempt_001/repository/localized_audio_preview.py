import os
from typing import Union

from openai import OpenAI


def generate_localized_audio_preview(text: str, *, voice: str = "alloy", model: str = "gpt-4o-mini-tts") -> Union[bytes, str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    try:
        return response.read()
    except Exception:
        return getattr(response, "content", "")