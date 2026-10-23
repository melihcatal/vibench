from google.cloud import speech_v1p1beta1 as speech
import os

def get_speech_client() -> speech.SpeechClient:
    """
    Returns a configured Google Cloud SpeechClient instance.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    gcloud is configured.
    """
    return speech.SpeechClient()


def get_audio_config(sample_rate_hertz: int = 16000,
                     encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
                     language_code: str = "en-US",
                     enable_automatic_punctuation: bool = True
) -> speech.RecognitionConfig:
    """
    Returns a RecognitionConfig for streaming speech recognition.
    """
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    return config

if __name__ == '__main__':
    # Example of client initialization
    # client = get_speech_client()
    # print(f"SpeechClient initialized: {client}")

    # Example of config generation
    # config = get_audio_config(language_code="fr-FR", enable_automatic_punctuation=False)
    # print(f"Generated RecognitionConfig: {config}")
    pass
