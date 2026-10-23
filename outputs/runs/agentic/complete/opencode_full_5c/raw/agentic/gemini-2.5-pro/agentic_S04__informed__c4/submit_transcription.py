from speech_client import client
from speech_models import TranscriptionJob
from assemblyai import Transcript


def submit_transcription_job(audio_path: str) -> str:
    """
    Submits an audio file for transcription and returns the job ID.
    """
    transcript: Transcript = client.transcripts.create(audio_path)
    return transcript.id
