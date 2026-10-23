import os
from pathlib import Path

import openai


def save_audio(text: str, output_path: str, model: str = "gpt-4o-mini-tts", voice: str = "alloy") -> str:
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    path = Path(output_path)
    response.stream_to_file(path)
    return str(path)
