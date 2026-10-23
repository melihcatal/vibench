import os
from google.cloud import speech_v1p1beta1 as speech


def transcribe_audio_sample(audio_content: bytes, language_code: str = "en-US") -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,  # Assuming a common sample rate, adjust if known
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    return transcript.strip()
