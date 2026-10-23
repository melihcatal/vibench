from speech_client import get_client
from speech_models import get_diarized_config


def diarized_transcript(audio_file: str) -> str:
    client = get_client()
    config = get_diarized_config()
    transcript_request = client.transcripts.request(audio_file, config)
    return transcript_request.id
