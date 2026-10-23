from speech_client import get_speech_client
from speech_models import TimestampedTranscript

def get_timestamped_transcript(job_id: str) -> TimestampedTranscript:
    """
    Returns word or segment timestamps from an AssemblyAI transcription result.
    """
    client = get_speech_client()
    
    transcript = client.transcripts.get(job_id)
    
    if transcript.status != "completed":
        raise Exception(f"Transcription job not completed. Current status: {transcript.status}")
    
    return TimestampedTranscript.from_assemblyai_words(transcript.words)