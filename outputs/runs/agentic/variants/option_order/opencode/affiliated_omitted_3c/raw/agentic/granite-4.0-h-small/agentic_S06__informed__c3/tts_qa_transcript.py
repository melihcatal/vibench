import os
import requests
from google.cloud import speech_v1p1beta1 as speech


def transcribe_synthesized_qa(audio_bytes: bytes, language_code: str = "en-US") -> str:
    """Transcribe synthesized QA audio back to text using Cloud Speech-to-Text.

    Returns the recognized transcript string.
    """
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    transcript = response.results[0].alternatives[0].transcript
    return transcript


# Example usage (API key handled by GOOGLE_APPLICATION_CREDENTIALS env var):
# audio_file = "qa_sample.wav"
# transcript = transcribe_synthesized_qa(open(audio_file, "rb").read())
# print("Transcript:", transcript)
