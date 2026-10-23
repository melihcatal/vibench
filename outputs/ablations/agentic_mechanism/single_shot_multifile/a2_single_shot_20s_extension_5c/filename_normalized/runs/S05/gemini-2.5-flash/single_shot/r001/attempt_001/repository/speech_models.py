from google.cloud.speech_v1p1beta1 import types

ENCODING = types.RecognitionConfig.AudioEncoding.LINEAR16
SAMPLE_RATE_HERTZ = 16000
LANGUAGE_CODE = "en-US"

def create_recognition_config(language_code, sample_rate_hertz, enable_automatic_punctuation):
    return types.RecognitionConfig(
        encoding=ENCODING,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

def create_streaming_recognition_config(recognition_config):
    return types.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )