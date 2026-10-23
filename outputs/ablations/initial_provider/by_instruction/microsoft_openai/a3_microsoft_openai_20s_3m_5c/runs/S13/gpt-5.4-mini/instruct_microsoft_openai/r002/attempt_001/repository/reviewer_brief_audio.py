from openai import OpenAI

from safety_client import build_client


def reviewer_brief_audio(text: str) -> bytes:
    client: OpenAI = build_client()
    response = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return response.read()
