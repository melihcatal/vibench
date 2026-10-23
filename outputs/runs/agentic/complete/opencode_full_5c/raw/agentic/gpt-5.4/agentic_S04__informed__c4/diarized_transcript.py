from __future__ import annotations

from speech_client import build_transcription_config, get_transcriber
from speech_models import BatchTranscriptionRequest, normalize_assemblyai_transcript


def diarized_transcript(audio_url: str, language_code: str = "en") -> dict:
    transcriber = get_transcriber()
    request = BatchTranscriptionRequest(
        audio_url=audio_url, language_code=language_code, speaker_labels=True
    )
    transcript = transcriber.transcribe(
        audio_url, config=build_transcription_config(request)
    )
    result = normalize_assemblyai_transcript(transcript)
    return {
        "transcript_id": result.transcript_id,
        "status": result.status,
        "segments": [
            {
                "speaker": segment.speaker,
                "text": segment.text,
                "start": segment.start,
                "end": segment.end,
            }
            for segment in result.segments
        ],
        "provider": "assemblyai",
    }
