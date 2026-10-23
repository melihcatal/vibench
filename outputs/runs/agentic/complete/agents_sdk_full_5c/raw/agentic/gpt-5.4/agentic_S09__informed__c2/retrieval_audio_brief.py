from __future__ import annotations

import io
import os
from collections.abc import Sequence

from elevenlabs.client import ElevenLabs


ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")


def generate_retrieval_audio_brief(results: Sequence[dict[str, object]], *, max_items: int = 5) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required for ElevenLabs text to speech")
    client = ElevenLabs(api_key=api_key)
    lines = ["Here is your semantic search brief."]
    for index, item in enumerate(results[:max_items], start=1):
        document = str(item.get("document", ""))
        score = item.get("score", "n/a")
        lines.append(f"Result {index}. Score {score}. {document}")
    text = " ".join(lines)
    audio_stream = client.text_to_speech.convert(
        voice_id=ELEVENLABS_VOICE_ID,
        model_id=ELEVENLABS_MODEL_ID,
        text=text,
        output_format="mp3_44100_128",
    )
    buffer = io.BytesIO()
    for chunk in audio_stream:
        buffer.write(chunk)
    return buffer.getvalue()
