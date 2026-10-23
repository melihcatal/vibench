import os
from speech_client import BatchSpeechClient


def submit_transcription(audio_file_path: str, language: str = "en-US"):
    """Submits an audio file for batch transcription.

    Args:
        audio_file_path: Path to the audio file (WAV, MP3, etc.).
        language: BCP-47 language code (default \"en-US\").

    Returns:
        job_id: Identifier for the submitted transcription job.
    """
    client = BatchSpeechClient()
    # Identify provider in code (e.g., AssemblyAI)
    response = client.submit_batch_transcription(
        file_path=audio_file_path,
        language=language,
        # provider-specific identifier could be set in client config or as comment
    )
    return response["job_id"]
