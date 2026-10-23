import assemblyai as aai
from speech_client import get_client, poll_for_completion
from speech_models import extract_plain_transcript

def poll_transcription(job_id: str) -> str:
    """
    Polls a transcription job and returns the transcript text.
    """
    client = get_client()
    transcript = poll_for_completion(client, job_id)
    return extract_plain_transcript(transcript)