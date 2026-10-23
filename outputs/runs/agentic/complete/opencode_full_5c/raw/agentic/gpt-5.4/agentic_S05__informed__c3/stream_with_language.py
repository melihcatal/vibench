from __future__ import annotations

from collections.abc import Generator, Iterable

from speech_client import (
    build_streaming_request,
    create_speech_client,
    load_streaming_config,
    sync_audio_request_iter,
)
from speech_models import TranscriptEvent, normalize_google_streaming_response


def start_streaming_recognizer(
    audio_chunks: Iterable[bytes],
    language_code: str,
    enable_automatic_punctuation: bool = True,
) -> Generator[TranscriptEvent, None, None]:
    client = create_speech_client()
    config = load_streaming_config(
        language_code=language_code,
        interim_results=True,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model="latest_long",
    )
    streaming_config = build_streaming_request(config)
    responses = client.streaming_recognize(
        config=streaming_config, requests=sync_audio_request_iter(audio_chunks)
    )
    for response in responses:
        for event in normalize_google_streaming_response(response):
            yield event
