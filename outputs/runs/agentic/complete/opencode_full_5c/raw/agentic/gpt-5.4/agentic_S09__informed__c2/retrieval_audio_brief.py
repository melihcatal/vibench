from __future__ import annotations

import os
from collections.abc import Sequence

from elevenlabs import ElevenLabs


def retrieval_audio_brief(
    results: Sequence[dict[str, object]], voice_id: str = "JBFqnCBsd6RMkjVDRZzb"
) -> bytes:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    summary_lines = []
    for index, item in enumerate(results, start=1):
        summary_lines.append(
            f"Result {index}: {item.get('document', '')}. Relevance score {item.get('score', 0)}."
        )
    text = " ".join(summary_lines)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        text=text,
    )
    return b"".join(audio)
