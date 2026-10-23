import os
from openai import OpenAI


def synthesize_text(
    text: str,
    model: str = "tts-1",
    voice: str = "alloy",
    response_format: str = "mp3",
    speed: float = 1.0,
) -> bytes:
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format=response_format,
        speed=speed,
    )
    return response.content
