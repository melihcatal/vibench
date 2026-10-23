import os
from google.cloud import speech_v1p1beta1 as speech


def transcribe_audio(
    audio_content: bytes, language_code: str = "en-US", sample_rate_hertz: int = 16000
) -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16 as a common output from TTS for transcription
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    return transcript.strip()
