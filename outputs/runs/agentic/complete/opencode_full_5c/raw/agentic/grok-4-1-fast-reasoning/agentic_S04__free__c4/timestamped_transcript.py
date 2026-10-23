import time
from typing import Optional, List, Dict
from assemblyai import TranscriptionStatus
from speech_client import get_speech_client
from speech_models import normalize_transcript


def get_word_timestamps(
    job_id: str,
    poll_interval: float = 5.0,
    timeout: int = 3600,
    api_key: Optional[str] = None,
) -> List[Dict[str, any]]:
    client = get_speech_client(api_key)
    start_time = time.time()
    while time.time() - start_time < timeout:
        transcript_raw = client.transcripts.get(job_id)
        if transcript_raw.status == TranscriptionStatus.completed:
            transcript = normalize_transcript(transcript_raw)
            return [
                {
                    "word": w.word,
                    "start": w.start,
                    "end": w.end,
                    "confidence": w.confidence,
                }
                for w in transcript.words
            ]
        elif transcript_raw.status in [
            TranscriptionStatus.error,
            TranscriptionStatus.failed,
        ]:
            raise ValueError(
                f"Transcription error: {getattr(transcript_raw, 'error', 'Unknown')}"
            )
        time.sleep(poll_interval)
    raise TimeoutError(f"Polling timed out after {timeout}s")
