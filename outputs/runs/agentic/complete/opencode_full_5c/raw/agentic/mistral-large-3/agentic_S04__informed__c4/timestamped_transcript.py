import os
from .speech_client import TranscriptionClient
from .speech_models import TimestampedTranscriptResponse

def get_timestamped_transcript(transcription_id: str) -> TimestampedTranscriptResponse:
    client = TranscriptionClient()
    transcript = client.client.get_transcript(transcription_id)
    if transcript.status != "completed":
        raise ValueError("Transcription not completed")
    
    words = []
    for word in transcript.words:
        words.append({
            "text": word.text,
            "start": word.start,
            "end": word.end,
            "confidence": word.confidence
        })
    
    return TimestampedTranscriptResponse(
        transcription_id=transcription_id,
        words=words