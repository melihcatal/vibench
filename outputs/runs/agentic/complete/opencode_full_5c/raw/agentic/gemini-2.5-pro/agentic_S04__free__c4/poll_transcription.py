from speech_client import SpeechClient
from speech_models import TranscriptionResponse


def poll_transcription_job(job_id: str) -> TranscriptionResponse:
    """
    Polls a transcription job from AssemblyAI and returns the result.
    """
    client = SpeechClient()
    response = client.poll_transcription(job_id)
    return response
