import os
from speech_client import BatchSpeechClient


def diarized_transcript(audio_path: str, num_speakers: int = 2) -> dict:
    """Request speaker diarization for a recorded meeting.

    Returns a transcript with speaker labels.
    """
    client = BatchSpeechClient()
    response = client.transcribe(
        audio_path=audio_path,
        model="assemblyai/diarized-speech-model",
        num_speakers=num_speakers,
    )
    return response.data  # transcript with speaker tags
