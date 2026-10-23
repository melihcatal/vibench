from __future__ import annotations

from typing import Iterable, Iterator

from partial_results import iter_transcript_events
from speech_client import build_streaming_config, get_speech_client, request_iter_from_chunks
from speech_models import StreamingConfig, TranscriptSegment



def start_streaming_recognizer(
    audio_chunks: Iterable[bytes],
    language_code: str,
    punctuation: bool = True,
) -> Iterator[TranscriptSegment]:
    client = get_speech_client()
    config = build_streaming_config(
        StreamingConfig(
            language_code=language_code,
            punctuation=punctuation,
            interim_results=True,
            model="latest_long",
        )
    )
    responses = client.streaming_recognize(config=config, requests=request_iter_from_chunks(audio_chunks))
    yield from iter_transcript_events(responses)
