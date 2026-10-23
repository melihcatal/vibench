from speech_client import get_speech_client
from speech_models import TranscriptionJob


def submit_transcription_job(audio_url: str) -> TranscriptionJob:
    """
    Submits an audio file for batch transcription using AssemblyAI.
    """
    client = get_speech_client()
    config = {"audio_url": audio_url}
    transcript = client.transcripts.submit(config)
    return TranscriptionJob(id=transcript.id, status=transcript.status)
