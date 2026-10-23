from speech_client import post
from speech_models import TranscriptionRequest


def submit_transcription(audio_url: str, language: str = None) -> dict:
    req = TranscriptionRequest(audio_url=audio_url, language=language)
    return post("/audio/transcriptions", req.to_payload())
