from speech_client import get_client
from speech_models import create_transcription_config

def submit_transcription(audio_file_path: str) -> str:
    client = get_client()
    config = create_transcription_config()
    transcript = client.transcripts.transcribe(audio_file_path, config)
    return transcript.id