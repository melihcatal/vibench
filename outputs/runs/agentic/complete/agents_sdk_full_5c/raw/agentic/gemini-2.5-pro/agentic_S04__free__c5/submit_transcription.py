from speech_client import get_transcriber

def submit_transcription_job(audio_url: str) -> str:
    """
    Submits a new transcription job to AssemblyAI.

    Args:
        audio_url: The public URL of the audio file to transcribe.

    Returns:
        The ID of the submitted transcription job.
    """
    transcriber = get_transcriber()
    transcript = transcriber.transcribe(audio_url)

    if transcript.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    return transcript.id
