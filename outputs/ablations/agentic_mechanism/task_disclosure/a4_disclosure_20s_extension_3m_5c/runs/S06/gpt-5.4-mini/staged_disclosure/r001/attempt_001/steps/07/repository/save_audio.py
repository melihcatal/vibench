import os
from typing import Optional, Union, BinaryIO

from openai import OpenAI


def save_audio(text: str, output: Union[str, BinaryIO], voice: str = "alloy", model: str = "gpt-4o-mini-tts") -> Optional[bytes]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    if hasattr(response, "read"):
        audio_bytes = response.read()
    else:
        audio_bytes = response.content
    if isinstance(output, str):
        with open(output, "wb") as f:
            f.write(audio_bytes)
        return None
    output.write(audio_bytes)
    return audio_bytes
