import os
from openai import OpenAI


def generate_platform_brief_audio(text: str) -> bytes:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=text
    )
    return speech.read()
