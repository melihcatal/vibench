import os

from openai import OpenAI


def reviewer_brief_audio(
    text: str, voice: str = "alloy", model: str = "gpt-4o-mini-tts"
):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    return response
