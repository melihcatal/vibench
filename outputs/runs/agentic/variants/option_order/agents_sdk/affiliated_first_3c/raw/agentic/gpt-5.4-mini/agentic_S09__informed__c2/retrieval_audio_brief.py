from __future__ import annotations

import os
import tempfile

from openai import OpenAI

from embeddings_client import load_config


def retrieval_audio_brief(results: list[dict[str, str]], voice: str = "alloy") -> bytes:
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key)
    brief = "\n".join(f"{item['title']}: {item['snippet']}" for item in results)
    speech = client.audio.speech.create(model="gpt-4o-mini-tts", voice=voice, input=f"Summarize these retrieval results: {brief}")
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        speech.stream_to_file(tmp.name)
        tmp.flush()
        tmp.seek(0)
        audio = tmp.read()
    os.unlink(tmp.name)
    return audio
