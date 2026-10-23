from __future__ import annotations

from typing import Any, Dict

from speech_client import get_transcriber, normalize_audio_source
from speech_models import TranscriptionRequest


def submit_transcription(audio_file: str, language_code: str | None = None) -> Dict[str, Any]:
    transcriber = get_transcriber()
    request = TranscriptionRequest(
        audio_source=audio_file,
        language_code=language_code,
        speaker_labels=False,
        words=True,
        paragraphs=True,
    )
    transcript = transcriber.transcribe(
        normalize_audio_source(request.audio_source),
        language_code=request.language_code,
        word_boost=None,
        speaker_labels=request.speaker_labels,
        punctuate=True,
        format_text=True,
        auto_highlights=False,
    )
    return {
        "transcript_id": transcript.id,
        "status": transcript.status,
        "request": request.to_dict(),
    }
