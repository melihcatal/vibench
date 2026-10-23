from __future__ import annotations

from typing import Iterable

from speech_client import get_google_speech_client, request_iter_from_chunks
from speech_models import (
    StreamingAudioChunk,
    StreamingSessionConfig,
    StreamingTranscriptEvent,
    transcript_events_from_google,
)


def stream_recognizer_with_language(
    audio_chunks: Iterable[bytes],
    language_code: str,
    enable_automatic_punctuation: bool = True,
) -> Iterable[StreamingTranscriptEvent]:
    session = StreamingSessionConfig(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        interim_results=True,
    )
    client = get_google_speech_client()
    wrapped_chunks = (StreamingAudioChunk(content=chunk) for chunk in audio_chunks)
    responses = client.streaming_recognize(
        requests=request_iter_from_chunks(wrapped_chunks, session)
    )
    for response in responses:
        yield from transcript_events_from_google(response)
