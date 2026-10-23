from __future__ import annotations

from typing import Iterable

from google.cloud import speech_v1 as speech

from speech_client import create_speech_client, request_iterator
from speech_models import (
    StreamSettings,
    StreamingAudioChunk,
    parse_google_streaming_response,
)


def start_language_stream(
    chunks: Iterable[StreamingAudioChunk],
    *,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    client = create_speech_client()
    config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
        ),
        interim_results=True,
    )
    responses = client.streaming_recognize(
        config=config, requests=request_iterator(chunks)
    )
    for response in responses:
        yield from parse_google_streaming_response(response)
