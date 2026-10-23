from assemblyai import Client, TranscriptionStatus
import time
from typing import List
from speech_client import get_assemblyai_api_key
from speech_models import Word


def get_word_timestamps(job_id: str) -> List[Word]:
    api_key = get_assemblyai_api_key()
    client = Client(api_key=api_key)
    transcript = client.transcripts.get(job_id)
    while transcript.status != TranscriptionStatus.completed:
        time.sleep(30)
        transcript = client.transcripts.get(job_id)
    if not hasattr(transcript, "words") or not transcript.words:
        return []
    return [
        {
            "text": w.text,
            "start": float(w.start),
            "end": float(w.end),
            "confidence": float(getattr(w, "confidence", 0.0)),
        }
        for w in transcript.words
    ]
