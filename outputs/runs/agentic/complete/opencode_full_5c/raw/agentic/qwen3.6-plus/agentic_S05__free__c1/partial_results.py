import asyncio
from typing import AsyncIterator, Callable, Awaitable

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_client import SpeechConfig, build_speech_client, build_recognition_config
from speech_models import (
    StreamingResult,
    normalize_streaming_result,
    build_streaming_event,
    StreamingEvent,
)


class PartialResultHandler:
    def __init__(
        self,
        on_interim: Callable[[StreamingResult], Awaitable[None]] | None = None,
        on_final: Callable[[StreamingResult], Awaitable[None]] | None = None,
        on_error: Callable[[str], Awaitable[None]] | None = None,
    ):
        self._on_interim = on_interim
        self._on_final = on_final
        self._on_error = on_error
        self._interim_buffer: list[StreamingResult] = []
        self._final_results: list[StreamingResult] = []

    async def handle_event(self, event: StreamingEvent) -> None:
        if event.error:
            if self._on_error:
                await self._on_error(event.error)
            return

        if event.result is None:
            return

        if event.event_type == "interim":
            self._interim_buffer.append(event.result)
            if self._on_interim:
                await self._on_interim(event.result)
        elif event.event_type == "final":
            self._interim_buffer.clear()
            self._final_results.append(event.result)
            if self._on_final:
                await self._on_final(event.result)

    @property
    def final_transcripts(self) -> list[str]:
        return [r.transcript for r in self._final_results]

    @property
    def latest_interim(self) -> str | None:
        return self._interim_buffer[-1].transcript if self._interim_buffer else None


async def process_partial_results(
    audio_chunks: AsyncIterator[bytes],
    config: SpeechConfig | None = None,
    on_interim: Callable[[StreamingResult], Awaitable[None]] | None = None,
    on_final: Callable[[StreamingResult], Awaitable[None]] | None = None,
    on_error: Callable[[str], Awaitable[None]] | None = None,
) -> PartialResultHandler:
    cfg = config or SpeechConfig()
    client = build_speech_client(cfg)
    recognition_config = build_recognition_config(cfg)
    handler = PartialResultHandler(
        on_interim=on_interim, on_final=on_final, on_error=on_error
    )

    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config
    )

    async def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunks:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        for result in response.results:
            normalized = normalize_streaming_result(result)
            event_type = "final" if normalized.is_final else "interim"
            event = build_streaming_event(event_type=event_type, result=normalized)
            await handler.handle_event(event)

    return handler
