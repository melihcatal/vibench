from __future__ import annotations

from openai import OpenAI

from embeddings_client import get_openai_client

TTS_MODEL = "gpt-4o-mini-tts"


def generate_spoken_brief(results: list[str]) -> str:
    client: OpenAI = get_openai_client()
    prompt = "Create a short spoken brief from these retrieved search results:\n" + "\n".join(results)
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice="alloy",
        input=prompt,
    )
    return f"Generated speech with model {TTS_MODEL}"
