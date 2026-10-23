from google.cloud.speech_v1p1beta1 import types
from speech_models import create_recognition_config, create_streaming_recognition_config, ENCODING

def create_language_streaming_recognizer_config(language_code, enable_automatic_punctuation, sample_rate_hertz):
    recognition_config = create_recognition_config(
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = create_streaming_recognition_config(recognition_config)
    return streaming_config