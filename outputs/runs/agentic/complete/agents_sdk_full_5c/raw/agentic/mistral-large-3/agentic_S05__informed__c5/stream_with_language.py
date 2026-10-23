from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamingConfig

async def start_stream_with_language(language_code="en-US", enable_punctuation=True):
    client = get_speech_client()
    config = StreamingConfig(
        language_code=language_code, enable_automatic_punctuation=enable_punctuation
    ).get_recognition_config()

    streaming_config = types.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    return client, streaming_config