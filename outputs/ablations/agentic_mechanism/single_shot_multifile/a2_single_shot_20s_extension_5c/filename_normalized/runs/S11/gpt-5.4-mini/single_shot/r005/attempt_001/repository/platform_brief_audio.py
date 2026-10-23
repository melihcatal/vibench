from openai import OpenAI
from model_client import get_platform_client


def platform_brief_audio(text: str):
    client = get_platform_client()
    response = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return response
