from speech_client import get_speech_client
import assemblyai

def submit_transcription_job(audio_url: str) -> str:
    """
    Submits an audio file URL for batch transcription.

    Args:
        audio_url: The public URL of the audio file to transcribe.

    Returns:
        The ID of the submitted transcription job.
    """
    transcriber = get_speech_client()
    transcript = transcriber.submit(audio_url)
    return transcript.id
