from speech_client import get_assemblyai_client
from speech_models import TimestampedTranscript

def get_timestamped_transcript(transcript_id: str) -> TimestampedTranscript:
    client = get_assemblyai_client()
    transcript = client.transcripts.get(transcript_id)
    if not transcript.words:
        raise ValueError("No word timestamps available.")
    
    return TimestampedTranscript(
        transcript_id=transcript.id,
        words=[
            {
                "text": word.text,
                "start": word.start,
                "end": word.end
            }
            for word in transcript.words
        ]
    )