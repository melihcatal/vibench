import os

from openai import OpenAI

BRIEF_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini")
VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")


def spoken_brief(text: str) -> bytes:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    speech = client.audio.speech.create(model=BRIEF_MODEL, voice=VOICE, input=text)
    return speech.read()
