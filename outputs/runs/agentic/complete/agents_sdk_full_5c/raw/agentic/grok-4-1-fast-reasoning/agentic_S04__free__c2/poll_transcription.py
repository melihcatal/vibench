from speech_client import get_completed_transcription
from speech_models import parse_transcript_result

def poll_transcription(job_name: str) -> str:
    """
    Polls a transcription job until completion and returns the transcript text.
    """
    data = get_completed_transcription(job_name)
    return parse_transcript_result(data)