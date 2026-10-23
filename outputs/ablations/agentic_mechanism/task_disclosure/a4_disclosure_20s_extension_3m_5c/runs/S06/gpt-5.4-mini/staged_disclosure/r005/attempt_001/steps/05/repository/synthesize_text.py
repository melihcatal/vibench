import os
import requests


def synthesize_text(text: str, voice: str = "alloy", model: str = "gpt-4o-mini-tts") -> bytes:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "voice": voice, "input": text, "format": "mp3"},
        timeout=60,
    )
    response.raise_for_status()
    return response.content
