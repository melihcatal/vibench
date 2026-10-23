import os
from typing import Any, Dict, Optional

from openai import OpenAI


def generate_spoken_preview(text: str, language: str = "en", voice: str = "alloy", model: str = "gpt-4o-mini-tts", output_format: str = "mp3", client: Optional[Any] = None) -> bytes:
    if not text:
        raise ValueError("text must not be empty")
    api_client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    instructions = f"Speak naturally in {language}."
    response = api_client.audio.speech.create(model=model, voice=voice, input=text, instructions=instructions, response_format=output_format)
    return response.read()


def generate_spoken_preview_to_file(text: str, output_path: str, language: str = "en", voice: str = "alloy", model: str = "gpt-4o-mini-tts", output_format: str = "mp3", client: Optional[Any] = None) -> str:
    audio_bytes = generate_spoken_preview(text=text, language=language, voice=voice, model=model, output_format=output_format, client=client)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path
