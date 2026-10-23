from __future__ import annotations

from typing import Iterable, Iterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import build_client, build_streaming_config, microphone_requests
from speech_models import SpeechStreamConfig


def stream_microphone(audio_frames: Iterable[bytes]) -> Iterator[str]:
    client = build_client()
    config = SpeechStreamConfig(language_code="en-US", punctuation=True, interim_results=True)
    requests = microphone_requests(audio_frames)
    responses = client.streaming_recognize(build_streaming_config(config), requests)
    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            yield result.alternatives[0].transcript


def stream_microphone_interim(audio_frames: Iterable[bytes]) -> Iterator[str]:
    client = build_client()
    config = SpeechStreamConfig(language_code="en-US", punctuation=True, interim_results=True)
    requests = microphone_requests(audio_frames)
    responses = client.streaming_recognize(build_streaming_config(config), requests)
    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            yield result.alternatives[0].transcript
