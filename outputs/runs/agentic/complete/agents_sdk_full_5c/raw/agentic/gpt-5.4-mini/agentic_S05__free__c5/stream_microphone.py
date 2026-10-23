from __future__ import annotations

from typing import Iterable

from google.cloud import speech_v1p1beta1 as speech

from speech_client import client


def stream_microphone(audio_frames: Iterable[bytes]):
    responses = client.recognize_stream(audio_frames, language_code="en-US", enable_punctuation=True, model="latest_long")
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript, not result.is_final
