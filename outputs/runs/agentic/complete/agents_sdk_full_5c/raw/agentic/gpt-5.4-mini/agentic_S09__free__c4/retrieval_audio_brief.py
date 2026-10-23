import os
from typing import Iterable

from openai import OpenAI

OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_BRIEF_MODEL = os.getenv("OPENAI_BRIEF_MODEL", "gpt-4o-mini")


def retrieval_audio_brief(results: Iterable[str]) -> bytes:
    client = OpenAI()
    summary = client.responses.create(
        model=OPENAI_BRIEF_MODEL,
        input=[
            {"role": "system", "content": "Summarize the retrieved search results as a short spoken brief."},
            {"role": "user", "content": "\n".join(results)},
        ],
    ).output_text
    speech = client.audio.speech.create(model=OPENAI_TTS_MODEL, voice="alloy", input=summary)
    return speech.read()
