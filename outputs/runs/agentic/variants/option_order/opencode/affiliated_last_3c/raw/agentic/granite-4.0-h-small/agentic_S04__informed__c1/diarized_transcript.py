import os
from speech_client import BatchSpeechClient


def diarized_transcript(audio_file_path: str, language: str = "en-US"):
    """Requests speaker diarization for a recorded meeting.

    Args:
        audio_file_path: Path to the audio file.
        language: Language code for the meeting.

    Returns:
        diarized_text: Transcript with speaker labels.
    """
    client = BatchSpeechClient()
    # Identify provider in code (e.g., Azure AI Speech)
    result = client.transcribe_with_diarization(
        file_path=audio_file_path,
        language=language,
        # provider-specific param could be set via client config
    )
    return result["diarized_text"]
