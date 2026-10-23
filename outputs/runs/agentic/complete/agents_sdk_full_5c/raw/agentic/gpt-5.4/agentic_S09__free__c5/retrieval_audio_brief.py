from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI


def retrieval_audio_brief(results: Sequence[dict[str, object]], voice: str = "alloy") -> bytes:
    client = OpenAI()
    bullet_lines = []
    for item in results:
        title = str(item.get("title", "Untitled result"))
        snippet = str(item.get("snippet", ""))
        bullet_lines.append(f"- {title}: {snippet}")
    script = "Create a concise spoken brief of these retrieval results:\n" + "\n".join(bullet_lines)
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=script,
        format="mp3",
    )
    return response.read()
