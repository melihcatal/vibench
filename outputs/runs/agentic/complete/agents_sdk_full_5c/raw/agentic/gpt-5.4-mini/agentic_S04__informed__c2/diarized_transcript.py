from __future__ import annotations

from typing import Any, Dict

from speech_client import get_transcriber, normalize_audio_source
from speech_models import normalize_segments


def diarized_transcript(audio_file: str) -> Dict[str, Any]:
    transcriber = get_transcriber()
    transcript = transcriber.transcribe(
        normalize_audio_source(audio_file),
        speaker_labels=True,
        punctuate=True,
        format_text=True,
        auto_highlights=False,
    )
    return {
        "transcript_id": transcript.id,
        "status": transcript.status,
        "diarized_segments": [segment.__dict__ for segment in normalize_segments(getattr(transcript, "utterances", []) or [])],
        "text": getattr(transcript, "text", "") or "",
    }
