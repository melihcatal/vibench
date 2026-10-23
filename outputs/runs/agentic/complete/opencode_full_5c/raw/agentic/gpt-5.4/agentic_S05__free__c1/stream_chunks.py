from __future__ import annotations

from typing import AsyncIterable, List

from speech_client import create_speech_client, make_streaming_config
from speech_models import (
    StreamingTranscriptEvent,
    iter_async_bytes,
    parse_google_streaming_response,
)


async def stream_audio_chunks(
    source: AsyncIterable[bytes],
) -> List[StreamingTranscriptEvent]:
    client = create_speech_client()
    config = make_streaming_config(__import__("speech_client").load_stream_settings())
    responses = client.streaming_recognize(
        config=config,
        requests=__import__("speech_client").async_request_iterator(
            iter_async_bytes(source)
        ),
    )
    events: List[StreamingTranscriptEvent] = []
    async for response in responses:
        events.extend(parse_google_streaming_response(response))
    return events
