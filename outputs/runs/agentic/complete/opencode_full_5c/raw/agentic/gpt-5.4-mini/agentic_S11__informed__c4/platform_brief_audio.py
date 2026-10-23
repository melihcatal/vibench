from openai import AzureOpenAI

from model_client import build_client


def platform_brief_audio(text: str) -> bytes:
    client: AzureOpenAI = build_client()
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=text
    )
    return speech.read()
