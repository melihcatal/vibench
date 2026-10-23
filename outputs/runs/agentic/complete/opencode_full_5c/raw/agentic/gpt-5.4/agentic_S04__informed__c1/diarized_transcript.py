from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import build_transcriber, build_transcription_config
from speech_models import TranscriptionSubmission, normalize_assemblyai_transcript


def diarized_transcript(
    audio_url: str,
    speakers_expected: Optional[int] = None,
    language_code: Optional[str] = None,
) -> Dict[str, Any]:
    request = TranscriptionSubmission(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
        speakers_expected=speakers_expected,
    )
    transcriber = build_transcriber()
    config = build_transcription_config(
        speaker_labels=True,
        speakers_expected=request.speakers_expected,
        language_code=request.language_code,
    )
    transcript = transcriber.transcribe(request.audio_url, config=config)
    normalized = normalize_assemblyai_transcript(transcript)
    return {
        "provider": "AssemblyAI",
        "job_id": normalized.job_id,
        "status": normalized.status,
        "transcript": normalized.text,
        "utterances": [
            {
                "speaker": segment.speaker,
                "text": segment.text,
                "start_ms": segment.start_ms,
                "end_ms": segment.end_ms,
                "confidence": segment.confidence,
            }
            for segment in normalized.segments
        ],
    }
