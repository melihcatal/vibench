from typing import Any, Dict

from speech_client import configure_client
from speech_models import TranscriptRequest, normalize_transcript_result


def diarized_transcript(audio_path: str) -> Dict[str, Any]:
    client = configure_client()
    request = TranscriptRequest(audio_url=audio_path, diarization=True)
    transcript = client.transcribe(
        request.audio_url,
        speaker_labels=True,
        punctuate=request.punctuate,
        format_text=request.format_text,
    )
    normalized = normalize_transcript_result(transcript)
    return {
        "transcript_id": normalized.transcript_id,
        "status": normalized.status,
        "segments": [segment.__dict__ for segment in normalized.segments],
    }
