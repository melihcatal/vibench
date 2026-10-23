from speech_client import get_speech_client
from speech_models import stt_config

def submit_transcription(audio_path: str) -> str:
    client = get_speech_client()
    audio_url = client.upload(audio_path)
    config = {
        'audio_url': audio_url,
        **stt_config()
    }
    transcript = client.transcripts.create(config)
    return transcript.id