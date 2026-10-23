from speech_client import poll_aai_transcription
from speech_models import TranscriptionResult


def poll_transcription_result(job_id: str) -> TranscriptionResult:
    """Polls a transcription job and returns the transcript result using AssemblyAI."""
    return poll_aai_transcription(job_id)
