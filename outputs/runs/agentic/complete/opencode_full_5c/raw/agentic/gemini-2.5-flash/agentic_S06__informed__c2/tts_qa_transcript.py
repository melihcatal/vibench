import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from speech_client import get_speech_to_text_client
from speech_models import TranscriptionRequest


def transcribe_audio(request: TranscriptionRequest) -> str:
    """Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text."""
    client = get_speech_to_text_client()

    audio = speech.RecognitionAudio(content=request.audio_content)

    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.MP3,  # Assuming MP3 for synthesized audio
        sample_rate_hertz=request.sample_rate_hertz,  # This should ideally be known from the TTS output
        language_code=request.language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript
