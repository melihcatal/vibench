from __future__ import annotations

from openai import OpenAI


def retrieval_audio_brief(results: list[str], voice: str = "alloy") -> bytes:
    client = OpenAI()
    prompt = "Create a short spoken brief of these retrieval results:\n- " + "\n- ".join(results)
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=prompt,
    )
    return response.read()
