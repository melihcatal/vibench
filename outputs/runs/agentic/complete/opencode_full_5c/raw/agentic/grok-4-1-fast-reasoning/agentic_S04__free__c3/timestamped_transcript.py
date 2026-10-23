from speech_client import get_speech_client
from assemblyai import TranscriptStatus
from typing import List, Dict, Any


def get_timestamps(job_id: str) -> List[Dict[str, Any]]:
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status != TranscriptStatus.completed:
        raise ValueError(
            f"Transcription job {job_id} not completed: {transcript.status}"
        )
    return [
        {
            "start": word.start / 1000.0,
            "end": word.end / 1000.0,
            "text": word.text,
            "confidence": getattr(word, "confidence", None),
        }
        for word in transcript.words
    ]
