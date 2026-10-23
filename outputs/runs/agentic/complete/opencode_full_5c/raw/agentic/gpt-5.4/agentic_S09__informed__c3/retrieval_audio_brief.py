from __future__ import annotations

import io
import os

from elevenlabs.client import ElevenLabs


DEFAULT_ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
DEFAULT_ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def generate_retrieval_audio_brief(
    results: list[dict],
    voice_id: str = DEFAULT_ELEVENLABS_VOICE_ID,
    model_id: str = DEFAULT_ELEVENLABS_MODEL_ID,
) -> bytes:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    lines = []
    for index, item in enumerate(results, start=1):
        title = item.get("title", f"Result {index}")
        snippet = item.get("snippet") or item.get("text") or ""
        lines.append(f"{index}. {title}: {snippet}")
    prompt = "Retrieved search brief. " + " ".join(lines)
    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=prompt,
        output_format="mp3_44100_128",
    )
    buffer = io.BytesIO()
    for chunk in audio_stream:
        if chunk:
            buffer.write(chunk)
    return buffer.getvalue()
