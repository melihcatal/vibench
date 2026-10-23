import os
from google.cloud import speech
from google.cloud import translate_v2 as translate
from google.cloud import language_v1
from google.cloud import aiplatform


def speech_client():
    return speech.SpeechClient()


def translate_client():
    return translate.Client()


def language_client():
    return language_v1.LanguageServiceClient()


def vertex_ai_init():
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    if project:
        aiplatform.init(project=project, location=location)


def speech_streaming_config(sample_rate_hz, language_code, enable_punctuation=False, enable_language=False):
    recognition = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hz,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )
    if enable_language:
        recognition = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hz,
            language_code=language_code,
            enable_automatic_punctuation=enable_punctuation,
        )
    return speech.StreamingRecognitionConfig(config=recognition, interim_results=True)
