from speech_client import get_speech_client
from speech_models import TranscriptionConfig


def submit_transcription_job(audio_url: str) -> str:
    """
    Submits a new transcription job to AssemblyAI.

    Args:
        audio_url: The public URL of the audio file to transcribe.

    Returns:
        The ID of the submitted transcription job.
    """
    aai = get_speech_client()
    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(
        language_code="en_us",
    )

    transcript = transcriber.submit(audio_url, config)
    return transcript.id
