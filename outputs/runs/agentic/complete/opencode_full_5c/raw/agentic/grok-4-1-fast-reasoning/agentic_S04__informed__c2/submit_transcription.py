from assemblyai import Client, TranscriptionConfig
from speech_client import get_assemblyai_api_key


def submit_transcription(audio_file: str) -> str:
    api_key = get_assemblyai_api_key()
    client = Client(api_key=api_key)
    config = TranscriptionConfig()
    transcript_input = client.transcripts.create(audio_file, config)
    return transcript_input.id
