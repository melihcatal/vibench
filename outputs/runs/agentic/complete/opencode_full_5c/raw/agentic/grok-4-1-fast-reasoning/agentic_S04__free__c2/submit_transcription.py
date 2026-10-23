from speech_client import get_client
from speech_models import get_standard_config


def submit_transcription(audio_file: str) -> str:
    client = get_client()
    config = get_standard_config()
    transcript_request = client.transcripts.request(audio_file, config)
    return transcript_request.id
