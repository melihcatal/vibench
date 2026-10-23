from speech_client import get_speech_client
from speech_models import normalize_transcript_response

def get_timestamped_transcript(job_id: str) -> list[dict]:
    """
    Returns word timestamps from a transcription result.
    """
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    normalized = normalize_transcript_response(transcript)
    return normalized["words"]
