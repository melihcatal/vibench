import os
from openai import OpenAI
from pathlib import Path

def generate_spoken_brief(text: str, output_path: str = "brief.mp3") -> None:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    speech_response.stream_to_file(output_path)