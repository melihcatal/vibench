import os
from pathlib import Path

from openai import OpenAI


def save_audio(text: str, output_path: str | None = None, *, voice: str = "alloy", model: str = "gpt-4o-mini-tts"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    audio_bytes = response.read()
    if output_path is None:
        return audio_bytes
    path = Path(output_path)
    path.write_bytes(audio_bytes)
    return str(path)
