from speech_client import post
from speech_models import TranscriptionRequest


def diarized_transcript(audio_url: str, language: str = None) -> dict:
    req = TranscriptionRequest(audio_url=audio_url, language=language, diarization=True)
    return post("/audio/transcriptions", req.to_payload())
