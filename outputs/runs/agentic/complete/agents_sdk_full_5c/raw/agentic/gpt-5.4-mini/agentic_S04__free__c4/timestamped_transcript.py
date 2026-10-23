from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from speech_client import OPENAI_TRANSCRIBE_MODEL, SpeechClientFactory
from speech_models import TranscriptionRequest, normalize_transcript


def timestamped_transcript(audio_path: str, granularity: str = "word", language: Optional[str] = None) -> Dict[str, Any]:
    client = SpeechClientFactory.create()
    req = TranscriptionRequest(
        audio_path=audio_path,
        model=OPENAI_TRANSCRIBE_MODEL,
        language=language,
        timestamp_granularities=[granularity],
    )
    with Path(req.audio_path).open("rb") as audio_file:
        result = client.audio.transcriptions.create(file=audio_file, **req.to_kwargs())
    normalized = normalize_transcript(result)
    timestamps = []
    for segment in normalized.segments:
        payload: Dict[str, Any] = {"start": segment.start, "end": segment.end, "text": segment.text}
        if segment.words:
            payload["words"] = segment.words
        timestamps.append(payload)
    return {"text": normalized.text, "timestamps": timestamps, "raw": normalized.raw}
