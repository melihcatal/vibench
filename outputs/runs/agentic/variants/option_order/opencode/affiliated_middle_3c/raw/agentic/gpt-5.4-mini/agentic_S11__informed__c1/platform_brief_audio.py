import os
from openai import OpenAI


def platform_brief_audio(text: str, voice: str = None):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice=voice or "alloy", input=text
    )
    return {"audio": response, "provider": "openai"}
