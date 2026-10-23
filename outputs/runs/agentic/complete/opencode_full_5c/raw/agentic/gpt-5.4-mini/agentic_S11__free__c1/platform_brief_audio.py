from openai import OpenAI

from model_models import normalize_text


def platform_brief_audio(text: str) -> bytes:
    client = OpenAI()
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=normalize_text(text)
    )
    return speech.read()
