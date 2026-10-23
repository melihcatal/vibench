import os
from pathlib import Path
from openai import OpenAI

def generate_spoken_brief(text: str, output_path: str, voice: str = "alloy") -> None:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
    )
    speech_response.stream_to_file(path)
