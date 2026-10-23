from google.cloud.speech_v1p1beta1 import types

# Define request type aliases used across streaming utilities
RecognitionConfig = types.RecognitionConfig
StreamingRecognitionConfig = types.StreamingRecognitionConfig
StreamingRecognizeRequest = types.StreamingRecognizeRequest


# Helper to build a basic config
def build_config(
    sample_rate_hertz=16000,
    language_code="en-US",
    enable_auto_punctuation=False,
    model="default",
) -> RecognitionConfig:
    return types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_auto_punctuation,
        model=model,
    )
