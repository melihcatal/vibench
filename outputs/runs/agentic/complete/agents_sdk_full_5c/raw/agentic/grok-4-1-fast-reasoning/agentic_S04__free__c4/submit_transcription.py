import assemblyai as aai
from speech_client import get_client

def submit_transcription(audio_url: str) -> str:
    """
    Submits an audio file for batch transcription.
    Returns the job ID.
    """
    client = get_client()
    config = aai.TranscriptionConfig(audio_url=audio_url)
    transcript = client.transcripts.create(config)
    return transcript.id