from speech_client import get_speech_client
from speech_models import diarized_config


def diarized_transcript(audio_path: str) -> str:
    client = get_speech_client()
    config = diarized_config()
    transcript = client.transcripts.transcribe(audio_path, config)
    return transcript.id
