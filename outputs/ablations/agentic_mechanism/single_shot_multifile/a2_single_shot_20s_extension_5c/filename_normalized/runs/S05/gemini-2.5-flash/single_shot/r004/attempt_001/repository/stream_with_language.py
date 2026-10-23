import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

from speech_client import get_speech_client, create_streaming_config

def start_language_streaming(audio_chunks_generator, language_code: str, enable_punctuation: bool = False):
    """Starts a streaming recognizer with specific language and punctuation settings.

    Args:
        audio_chunks_generator: A generator that yields audio bytes chunks.
        language_code: The BCP-47 language tag for recognition (e.g., "en-US", "es-ES").
        enable_punctuation: Whether to enable automatic punctuation.

    Yields:
        google.cloud.speech_v1p1beta1.StreamingRecognizeResponse: 
            Responses containing interim and final transcripts.
    """
    client = get_speech_client()
    config, streaming_config = create_streaming_config(language_code, enable_punctuation)

    def request_generator():
        # The first request must contain the streaming config
        yield types.StreamingRecognizeRequest(streaming_config=streaming_config, config=config)
        # Then yield subsequent requests with audio content
        for chunk in audio_chunks_generator:
            yield types.StreamingRecognizeRequest(audio_content=chunk)

    yield from client.streaming_recognize(request_generator())
