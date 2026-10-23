import assemblyai as aai
from speech_client import get_client

def timestamped_transcript(job_id: str) -> list:
    client = get_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status != aai.TranscriptStatus.completed:
        raise ValueError("Job not completed")
    return [
        {
            "word": word.word,
            "start": word.start,
            "end": word.end,
            "confidence": getattr(word, 'confidence', None)
        }
        for word in transcript.words
    ]