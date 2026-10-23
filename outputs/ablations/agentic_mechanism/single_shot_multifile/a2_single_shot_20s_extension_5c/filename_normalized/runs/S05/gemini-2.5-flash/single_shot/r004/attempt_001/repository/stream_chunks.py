import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

from speech_client import get_speech_client, create_streaming_config

def recognize_async_audio_chunks(audio_chunks_iterable, language_code: str = "en-US", enable_punctuation: bool = True):
    """Transcribes a stream of audio chunks using Google Cloud Speech-to-Text.

    Args:
        audio_chunks_iterable: An iterable (e.g., generator) that yields audio bytes chunks.
        language_code: The language code for recognition (e.g., "en-US").
        enable_punctuation: Whether to enable automatic punctuation.

    Yields:
        google.cloud.speech_v1p1beta1.StreamingRecognizeResponse: 
            Responses containing interim and final transcripts.
    """
    client = get_speech_client()
    config, streaming_config = create_streaming_config(language_code, enable_punctuation)

    def request_generator():
        # Yield the first request with the config
        yield types.StreamingRecognizeRequest(streaming_config=streaming_config, config=config)
        # Then yield subsequent requests with audio content
        for chunk in audio_chunks_iterable:
            yield types.StreamingRecognizeRequest(audio_content=chunk)

    yield from client.streaming_recognize(request_generator())
