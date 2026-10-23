from __future__ import annotations

from collections.abc import Iterable
from typing import Iterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import SpeechConfig, build_streaming_config, get_speech_client


def stream_with_language(language_code: str = "en-US") -> Iterator[str]:
    client = get_speech_client()
    config = build_streaming_config(SpeechConfig(language_code=language_code, enable_automatic_punctuation=True, model="latest_long"))
    audio = [speech.StreamingRecognizeRequest(audio_content=b"")]
    responses = client.streaming_recognize(config=config, requests=audio)
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
