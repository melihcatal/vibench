import os
from openai import OpenAI
from model_models import normalize_text


def spoken_brief(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=normalize_text(text)
    )
    return resp
