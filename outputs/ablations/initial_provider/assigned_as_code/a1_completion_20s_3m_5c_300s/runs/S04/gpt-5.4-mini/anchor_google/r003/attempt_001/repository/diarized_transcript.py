from google.cloud import speech

from speech_client import build_recognition_config, get_client
from speech_models import normalize_segments


def diarized_transcript(payload, config=None):
    client = get_client()
    response = client.recognize(
        config=build_recognition_config({**(config or {}), **payload, "diarization": True}),
        audio=speech.RecognitionAudio(uri=payload["audio_uri"]),
    )
    return {
        "status": "COMPLETED",
        "segments": normalize_segments(response.results),
    }
