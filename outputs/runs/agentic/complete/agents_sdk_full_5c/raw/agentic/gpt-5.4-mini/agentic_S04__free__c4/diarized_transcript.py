from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from speech_client import OPENAI_TRANSCRIBE_MODEL, SpeechClientFactory
from speech_models import TranscriptionRequest, normalize_transcript


def diarized_transcript(audio_path: str, language: Optional[str] = None) -> Dict[str, Any]:
    client = SpeechClientFactory.create()
    req = TranscriptionRequest(audio_path=audio_path, model=OPENAI_TRANSCRIBE_MODEL, language=language, diarize=True)
    with Path(req.audio_path).open("rb") as audio_file:
        result = client.audio.transcriptions.create(file=audio_file, **req.to_kwargs())
    normalized = normalize_transcript(result)
    return {"text": normalized.text, "segments": [segment.__dict__ for segment in normalized.segments], "raw": normalized.raw}
