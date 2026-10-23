"""Stream audio chunks from an async source using Google Cloud Speech-to-Text."""

import asyncio
import queue
import threading
from typing import AsyncIterator, Iterator, Tuple

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types as speech_types

from speech_client import get_speech_client, build_streaming_config
from partial_results import handle_recognition_event

ENCODING = speech_types.RecognitionConfig.AudioEncoding.LINEAR16
_CHUNK_TIMEOUT = 1.0


def _audio_chunk_iterator(audio_queue: queue.Queue, stop_event: threading.Event) -> Iterator[bytes]:
    """Bridge an async audio queue to a sync iterator for the streaming client."""
    while not stop_event.is_set() or not audio_queue.empty():
        try:
            chunk = audio_queue.get(timeout=_CHUNK_TIMEOUT)
            yield chunk
        except queue.Empty:
            continue


async def stream_chunks_transcription(
    audio_source: AsyncIterator[bytes],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    enable_punctuation: bool = True,
) -> AsyncIterator[Tuple[str, bool, float]]:
    """Stream audio chunks from an async source and yield transcription events.

    Uses Google Cloud Speech-to-Text streaming_recognize with a bridge between
    the async audio source and the synchronous streaming client.

    Args:
        audio_source: Async iterator yielding raw audio bytes chunks.
        language_code: BCP-47 language code for recognition.
        sample_rate_hertz: Audio sample rate in Hz.
        enable_punctuation: Whether to enable automatic punctuation.

    Yields:
        Tuples of (transcript, is_final, confidence) for each recognition result.
    """
    client = get_speech_client()
    config = build_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        encoding=ENCODING,
        sample_rate_hertz=sample_rate_hertz,
    )

    streaming_config = speech_types.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    audio_queue: queue.Queue = queue.Queue()
    stop_event = threading.Event()
    result_queue: queue.Queue = queue.Queue()

    async def _feed_queue():
        """Pump async audio source into the sync queue."""
        async for chunk in audio_source:
            audio_queue.put(chunk)
        stop_event.set()

    def _run_recognition():
        """Run the synchronous Google Cloud Speech streaming_recognize call."""
        chunk_iter = _audio_chunk_iterator(audio_queue, stop_event)
        requests = (
            speech_types.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in chunk_iter
        )
        responses = client.streaming_recognize(
            config=streaming_config,
            requests=requests,
        )
        for response in responses:
            for result in response.results:
                for transcript, is_final, confidence in handle_recognition_event(result):
                    result_queue.put((transcript, is_final, confidence))
        result_queue.put(None)  # Sentinel

    feed_task = asyncio.create_task(_feed_queue())
    recognition_thread = threading.Thread(target=_run_recognition, daemon=True)
    recognition_thread.start()

    try:
        loop = asyncio.get_event_loop()
        while True:
            item = await loop.run_in_executor(None, result_queue.get)
            if item is None:
                break
            yield item
    finally:
        stop_event.set()
        await feed_task
        recognition_thread.join(timeout=5)
