from __future__ import annotations

from pathlib import Path

from speech_client import OPENAI_TRANSCRIPTION_MODEL, get_openai_client


def transcribe_qa_sample(audio_path: str | Path) -> dict:
    client = get_openai_client()
    path = Path(audio_path)
    with path.open("rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=OPENAI_TRANSCRIPTION_MODEL,
            file=audio_file,
        )
    return {
        "provider": "openai",
        "model": OPENAI_TRANSCRIPTION_MODEL,
        "text": transcript.text,
        "audio_path": str(path),
    }
