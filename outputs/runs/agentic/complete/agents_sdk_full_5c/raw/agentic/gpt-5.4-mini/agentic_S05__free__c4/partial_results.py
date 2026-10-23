from __future__ import annotations

from typing import Iterable, Iterator, Tuple

from google.cloud import speech_v1p1beta1 as speech

from speech_client import build_client, build_streaming_config, microphone_requests
from speech_models import NormalizedEvent, SpeechStreamConfig, normalize_event


def partial_results(audio_frames: Iterable[bytes]) -> Iterator[Tuple[str, bool]]:
    client = build_client()
    config = SpeechStreamConfig(language_code="en-US", punctuation=True, interim_results=True)
    responses = client.streaming_recognize(build_streaming_config(config), microphone_requests(audio_frames))
    for response in responses:
        for result in response.results:
            payload = {
                "transcript": result.alternatives[0].transcript if result.alternatives else "",
                "is_final": getattr(result, "is_final", False),
            }
            event: NormalizedEvent = normalize_event(payload)
            yield event.transcript, event.is_final
