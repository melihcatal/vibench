from speech_client import get_speech_client
from assemblyai import Transcriber


def submit_transcription_job(audio_url: str) -> str:
    """
    Submits a transcription job to AssemblyAI.
    """
    client = get_speech_client()
    transcriber = Transcriber(client=client)
    transcript = transcriber.transcribe(audio_url)
    return transcript.id
