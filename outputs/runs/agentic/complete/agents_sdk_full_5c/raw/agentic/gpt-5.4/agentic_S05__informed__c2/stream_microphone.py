from __future__ import annotations

from typing import Iterable, Iterator

from google.cloud import speech

from partial_results import iter_transcript_events
from speech_client import build_streaming_config, get_speech_client, request_iter_from_chunks
from speech_models import StreamingConfig, TranscriptSegment



def stream_microphone(audio_chunks: Iterable[bytes]) -> Iterator[TranscriptSegment]:
    client = get_speech_client()
    config = build_streaming_config(StreamingConfig(interim_results=True, model="latest_long"))
    requests = request_iter_from_chunks(audio_chunks)
    responses = client.streaming_recognize(config=config, requests=requests)
    yield from iter_transcript_events(responses)
