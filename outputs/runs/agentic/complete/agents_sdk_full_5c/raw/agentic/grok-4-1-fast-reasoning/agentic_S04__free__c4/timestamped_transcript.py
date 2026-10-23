import assemblyai as aai
from speech_client import get_client, poll_for_completion
from speech_models import extract_word_timestamps

def timestamped_transcript(job_id: str) -> list:
    """
    Returns word timestamps from a transcription result.
    Polls if not completed.
    """
    client = get_client()
    transcript = poll_for_completion(client, job_id)
    return extract_word_timestamps(transcript)