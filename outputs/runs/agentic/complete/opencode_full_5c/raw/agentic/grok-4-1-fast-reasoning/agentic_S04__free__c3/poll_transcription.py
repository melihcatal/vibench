from speech_client import get_speech_client
from assemblyai import TranscriptStatus
from typing import Dict, Any


def poll_transcription(job_id: str) -> Dict[str, Any]:
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status != TranscriptStatus.completed:
        raise ValueError(f"Transcription job {job_id} status: {transcript.status}")
    return {
        "text": transcript.text,
        "confidence": transcript.confidence,
        "full": transcript.json_response,
    }
