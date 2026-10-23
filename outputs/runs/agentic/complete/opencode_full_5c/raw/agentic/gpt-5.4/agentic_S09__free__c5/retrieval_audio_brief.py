from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI


def retrieval_audio_brief(
    results: Sequence[dict], voice: str = "alloy", model: str = "gpt-4o-mini-tts"
) -> dict:
    client = OpenAI(
        api_key=__import__("os").getenv("OPENAI_API_KEY"),
        base_url=__import__("os").getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        ),
    )
    summary_lines = []
    for item in results:
        title = item.get("title") or item.get("document") or "Untitled result"
        snippet = item.get("snippet") or item.get("summary") or ""
        summary_lines.append(f"- {title}: {snippet}".strip())
    input_text = (
        "Create a concise spoken retrieval brief from these results:\n"
        + "\n".join(summary_lines)
    )
    audio = client.audio.speech.create(
        model=model,
        voice=voice,
        input=input_text,
        format="mp3",
    )
    return {
        "provider": "openai",
        "model": model,
        "voice": voice,
        "audio_bytes": audio.read(),
    }
