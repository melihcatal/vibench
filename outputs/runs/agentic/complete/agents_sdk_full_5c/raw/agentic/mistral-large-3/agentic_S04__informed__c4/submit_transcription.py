import os
from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest


def submit_transcription(audio_url: str, speaker_labels: bool = False) -> str:
    """
    Submit an audio file for batch transcription using AssemblyAI.
    Returns the transcription job ID.
    """
    client = get_assemblyai_client()
    request = TranscriptionRequest(
        audio_url=audio_url,
        speaker_labels=speaker_labels,
        language_code="en"
    )
    transcript = client.transcripts.create(**request.dict())
    return transcript.id