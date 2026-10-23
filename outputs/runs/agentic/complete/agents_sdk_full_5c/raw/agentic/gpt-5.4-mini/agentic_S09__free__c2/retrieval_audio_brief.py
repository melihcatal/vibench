import os

from openai import OpenAI

OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def generate_spoken_brief(retrieved_results: list[str]) -> bytes:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brief = "Summary of retrieved results: " + "; ".join(retrieved_results)
    speech = client.audio.speech.create(model=OPENAI_TTS_MODEL, voice="alloy", input=brief)
    return speech.read()
