import asyncio
from typing import AsyncIterator, AsyncGenerator, Optional, Callable

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

from speech_client import (
    create_speech_client,
    build_streaming_config,
    GOOGLE_SPEECH_API_ENDPOINT,
    DEFAULT_MODEL,
)
from speech_models import (
    RecognitionResult,
    normalize_google_response,
    StreamConfig,
)


class AsyncAudioSource:
    def __init__(
        self,
        queue: asyncio.Queue,
        sample_rate: int = 16000,
        encoding: str = "LINEAR16",
    ):
        self.queue = queue
        self.sample_rate = sample_rate
        self.encoding = encoding
        self._closed = False

    async def read_chunk(self) -> Optional[bytes]:
        if self._closed:
            return None
        chunk = await self.queue.get()
        if chunk is None:
            self._closed = True
            return None
        return chunk

    def close(self):
        self._closed = True

    async def put_audio(self, audio_bytes: bytes):
        await self.queue.put(audio_bytes)

    async def signal_end(self):
        await self.queue.put(None)


async def chunk_iterator(
    source: AsyncAudioSource,
) -> AsyncIterator[bytes]:
    while True:
        chunk = await source.read_chunk()
        if chunk is None:
            break
        yield chunk


async def stream_chunks_to_recognizer(
    source: AsyncAudioSource,
    project_id: str,
    model: str = DEFAULT_MODEL,
    language_code: str = "en-US",
) -> AsyncGenerator[RecognitionResult, None]:
    client = create_speech_client()
    config = build_streaming_config(
        project_id=project_id,
        model=model,
        language_code=language_code,
    )

    async def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=config["recognizer"],
            streaming_config=config["config"],
        )
        async for chunk in chunk_iterator(source):
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        if response.results:
            result = normalize_google_response(response)
            yield result


async def stream_chunks_with_progress(
    source: AsyncAudioSource,
    project_id: str,
    on_result: Callable[[RecognitionResult], None],
    model: str = DEFAULT_MODEL,
    language_code: str = "en-US",
    on_complete: Optional[Callable[[], None]] = None,
):
    async for result in stream_chunks_to_recognizer(
        source=source,
        project_id=project_id,
        model=model,
        language_code=language_code,
    ):
        on_result(result)

    if on_complete:
        on_complete()
