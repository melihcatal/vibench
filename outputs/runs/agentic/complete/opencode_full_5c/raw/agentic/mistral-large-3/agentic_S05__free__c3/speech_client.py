from google.cloud import speech_v1p1beta1 as speech
from google.api_core.client_options import ClientOptions
import os


def get_speech_client():
    client_options = ClientOptions(
        api_endpoint=os.getenv("GOOGLE_SPEECH_API_ENDPOINT", "speech.googleapis.com")
    )
    return speech.SpeechClient(client_options=client_options)


def get_streaming_config(
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    model: str = "latest_long",
) -> speech.StreamingRecognitionConfig:
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        model=model,
    )
    return speech.StreamingRecognitionConfig(config=config, interim_results=True)
