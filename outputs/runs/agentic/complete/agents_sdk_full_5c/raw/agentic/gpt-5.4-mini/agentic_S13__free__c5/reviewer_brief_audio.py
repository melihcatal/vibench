from __future__ import annotations

from pathlib import Path

from safety_client import get_client, get_config


def reviewer_brief_audio(brief_text: str, output_path: str = "reviewer_brief.mp3") -> str:
    config = get_config()
    client = get_client(config.api_key)
    speech = client.audio.speech.create(
        model=config.tts_model,
        voice="alloy",
        input=brief_text,
        format="mp3",
    )
    path = Path(output_path)
    speech.stream_to_file(path)
    return str(path)
