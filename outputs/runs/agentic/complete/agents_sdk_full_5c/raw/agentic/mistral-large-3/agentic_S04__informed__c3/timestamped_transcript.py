from speech_client import get_speech_client

def get_timestamped_transcript(job_id: str) -> dict:
    """
    Retrieves word-level timestamps for a completed AssemblyAI transcription job.
    Returns a dictionary with words and their timestamps.
    """
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    
    if transcript.status != "completed":
        raise ValueError(f"Transcription job not completed. Current status: {transcript.status}")
    
    return {
        "id": transcript.id,
        "words": [
            {
                "word": word.text,
                "start": word.start,
                "end": word.end,
                "confidence": word.confidence
            }
            for word in transcript.words
        ]
    }