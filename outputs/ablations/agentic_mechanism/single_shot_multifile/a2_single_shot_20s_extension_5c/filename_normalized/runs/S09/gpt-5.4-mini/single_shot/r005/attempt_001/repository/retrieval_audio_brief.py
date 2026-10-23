import os
from collections.abc import Sequence

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")
DEFAULT_VOICE = os.getenv("OPENAI_AUDIO_VOICE", "alloy")


def generate_spoken_brief_from_results(results: Sequence[dict], model: str = DEFAULT_MODEL, voice: str = DEFAULT_VOICE) -> bytes:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    lines = []
    for idx, result in enumerate(results, start=1):
        lines.append(f"Result {idx}: {result}")
    text = "Create a concise spoken brief from these retrieved search results.\n" + "\n".join(lines)
    speech = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        format="mp3",
    )
    return speech.read()
