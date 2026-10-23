from __future__ import annotations

from openai import OpenAI

from embeddings_client import load_settings


def retrieval_audio_brief(results: list[str]) -> bytes:
    settings = load_settings()
    client = OpenAI()
    brief_text = client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {"role": "system", "content": "Write a concise spoken brief from retrieved search results."},
            {"role": "user", "content": "\n".join(results)},
        ],
    ).choices[0].message.content.strip()
    speech = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=brief_text)
    return speech.read()
