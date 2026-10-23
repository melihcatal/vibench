from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


async def stream_with_language(
    language_code: str = "en-US", enable_punctuation: bool = True
):
    """Starts a streaming recognizer with language and punctuation settings."""
    client = get_speech_client()
    config = StreamingRecognitionConfig(
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        interim_results=True,
    )

    streaming_config = types.StreamingRecognitionConfig(
        config=config.to_grpc(),
        interim_results=True,
    )

    return client, streaming_config
