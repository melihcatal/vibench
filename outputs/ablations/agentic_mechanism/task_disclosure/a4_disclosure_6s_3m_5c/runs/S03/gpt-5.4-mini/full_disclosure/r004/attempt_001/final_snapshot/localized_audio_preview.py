import os
from typing import Optional

from openai import OpenAI


def generate_spoken_preview(text: str, voice: str = "alloy", model: str = "gpt-4o-mini-tts", output_file: Optional[str] = None) -> bytes:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    audio = client.audio.speech.create(model=model, voice=voice, input=text)
    data = audio.read()
    if output_file:
        with open(output_file, "wb") as f:
            f.write(data)
    return data
