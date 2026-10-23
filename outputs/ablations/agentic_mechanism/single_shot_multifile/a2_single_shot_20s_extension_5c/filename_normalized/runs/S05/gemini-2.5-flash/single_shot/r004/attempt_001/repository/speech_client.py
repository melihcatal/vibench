import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

def get_speech_client():
    """Returns an initialized Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()

def create_streaming_config(
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    sample_rate_hertz: int = 16000,
    encoding: enums.RecognitionConfig.AudioEncoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,
    model: str = "default", # Can be "default", "command_and_search", "medical_dictation", "phone_call", "video", "telephony"
    use_enhanced: bool = False
):
    """Creates a Google Cloud Speech-to-Text RecognitionConfig and StreamingRecognitionConfig.

    Args:
        language_code: The language code (e.g., "en-US").
        enable_automatic_punctuation: Whether to enable automatic punctuation.
        sample_rate_hertz: The audio sample rate.
        encoding: The audio encoding.
        model: The model to use for recognition.
        use_enhanced: Whether to use an enhanced model.

    Returns:
        Tuple[types.RecognitionConfig, types.StreamingRecognitionConfig]:
            The recognition and streaming configuration objects.
    """
    config = types.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
        use_enhanced=use_enhanced
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
    return config, streaming_config
