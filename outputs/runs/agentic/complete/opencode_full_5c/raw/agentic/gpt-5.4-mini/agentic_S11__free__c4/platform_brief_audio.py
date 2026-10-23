import os

from openai import OpenAI


def platform_brief_audio(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=text
    )
