from speech_client import get_speech_client
from speech_models import normalize_transcript_response

def poll_transcription(job_id: str) -> dict:
    """
    Poll a transcription job and return the normalized transcript.
    """
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    return normalize_transcript_response(transcript)
