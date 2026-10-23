from speech_client import get_speech_client
from speech_models import basic_config


def submit_transcription(audio_path: str) -> str:
    client = get_speech_client()
    config = basic_config()
    transcript = client.transcripts.transcribe(audio_path, config)
    return transcript.id
