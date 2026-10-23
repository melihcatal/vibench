from __future__ import annotations

from speech_client import get_transcriber
from speech_models import SpeechRequest, normalize_transcript


def timestamped_transcript(request: SpeechRequest):
    transcriber = get_transcriber()
    transcript = transcriber.transcribe(
        request.audio_path or request.audio_url,
        {
            "speaker_labels": request.speaker_labels,
            "punctuate": True,
            "format_text": True,
            "language_code": request.language_code,
            "word_timestamps": True,
        },
    )
    return normalize_transcript(transcript)
