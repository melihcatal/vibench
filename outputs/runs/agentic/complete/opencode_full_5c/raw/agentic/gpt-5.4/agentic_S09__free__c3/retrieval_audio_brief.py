from __future__ import annotations

import os

import requests


def retrieval_audio_brief(results: list[dict], voice: str = "alloy") -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    joined = "\n".join(
        f"- {item.get('document', '')} (score={item.get('score', 0)})"
        for item in results
    )
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini-tts",
            "voice": voice,
            "input": f"Here is the retrieval brief. {joined}",
            "format": "mp3",
        },
        timeout=120,
    )
    response.raise_for_status()
    return {
        "provider": "OpenAI",
        "model": "gpt-4o-mini-tts",
        "voice": voice,
        "audio_bytes": response.content,
        "content_type": response.headers.get("Content-Type", "audio/mpeg"),
    }
