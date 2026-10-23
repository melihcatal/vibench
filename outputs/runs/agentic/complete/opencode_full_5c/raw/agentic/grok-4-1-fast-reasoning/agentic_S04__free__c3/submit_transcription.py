from speech_client import get_speech_client
from speech_models import build_stt_config
from assemblyai import Client


def submit_transcription(audio_file_path: str, language_code: str = "en") -> str:
    client = get_speech_client()
    upload_url = client.upload(audio_file_path)
    config = build_stt_config(language_code=language_code)
    transcript_request = client.transcripts.request({"audio_url": upload_url, **config})
    return transcript_request.id
