from __future__ import annotations

from typing import Iterable, List

from elevenlabs import ElevenLabs

DEFAULT_VOICE_ID = "Rachel"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def generate_spoken_brief(results: List[dict], voice_id: str = DEFAULT_VOICE_ID) -> bytes:
    client = ElevenLabs()
    brief = " ".join(str(item.get("summary", item.get("text", ""))) for item in results)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=DEFAULT_MODEL_ID,
        text=brief,
    )
    return b"".join(audio)
