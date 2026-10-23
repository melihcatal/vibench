from __future__ import annotations

from typing import AsyncIterable, List

from google.cloud import speech

from partial_results import collect_transcript_events
from speech_client import async_request_iter_from_source, build_streaming_config, get_speech_client
from speech_models import StreamChunk, StreamingConfig, TranscriptSegment


async def stream_audio_chunks(source: AsyncIterable[bytes | StreamChunk]) -> List[TranscriptSegment]:
    client = get_speech_client()
    config = build_streaming_config(StreamingConfig(interim_results=True, model="latest_long"))
    requests = async_request_iter_from_source(source)
    responses = client.streaming_recognize(config=config, requests=requests)
    return await collect_transcript_events(responses)
