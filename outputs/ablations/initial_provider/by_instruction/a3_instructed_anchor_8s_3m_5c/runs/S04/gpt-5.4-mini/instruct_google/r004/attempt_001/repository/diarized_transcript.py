from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client, make_long_running_config
from speech_models import TranscriptionRequest, normalize_segments


def diarized_transcript(audio_uri: str, language_code: str = "en-US"):
    client = get_speech_client()
    request = TranscriptionRequest(audio_uri=audio_uri, language_code=language_code, enable_diarization=True)
    audio = speech.RecognitionAudio(uri=request.audio_uri)
    config = speech.RecognitionConfig(**make_long_running_config(request.language_code, enable_diarization=True))
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result()
    return normalize_segments(response)
