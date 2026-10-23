from speech_client import get_speech_client
from speech_models import TranscriptionRequest
from google.cloud import speech


def transcribe_audio(request: TranscriptionRequest) -> str:
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=request.audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=request.language_code,
    )

    response = client.recognize(config=config, audio=audio)

    if response.results:
        return response.results[0].alternatives[0].transcript
    return ""
