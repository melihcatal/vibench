import os
from functools import lru_cache
from typing import Optional, AsyncIterator

from google.cloud.speech_v1p1beta1 import SpeechClient
from google.cloud.speech_v1p1beta1.types import RecognitionConfig, StreamingRecognizeRequest
from speech_models import AudioChunk

@lru_cache(maxsize=1)
def get_speech_client() -> SpeechClient:
    return SpeechClient()

def get_streaming_config(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    encoding: RecognitionConfig.AudioEncoding = RecognitionConfig.AudioEncoding.LINEAR16,
    enable_automatic_punctuation: bool = True,
    model: str = "default",
    profanity_filter: bool = False,
    enable_word_time_offsets: bool = False,
    use_enhanced: bool = False,
    speech_contexts: Optional[list] = None
) -> RecognitionConfig:
    config = RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
        profanity_filter=profanity_filter,
        enable_word_time_offsets=enable_word_time_offsets,
        use_enhanced=use_enhanced,
    )
    if speech_contexts:
        config.speech_contexts.extend(speech_contexts)
    return config
