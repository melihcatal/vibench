from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator, Callable

from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents

from speech_client import create_deepgram_client, build_streaming_options
from speech_models import TranscriptResult, normalize_deepgram_result, StreamingEvent

logger = logging.getLogger(__name__)


class PartialResultsHandler:
    def __init__(
        self,
        client: DeepgramClient | None = None,
        language: str | None = None,
        model: str | None = None,
    ):
        self.client = client or create_deepgram_client()
        self.language = language
        self.model = model
        self._interim_buffer: list[TranscriptResult] = []
        self._final_results: list[TranscriptResult] = []
        self._on_interim: Callable[[TranscriptResult], None] | None = None
        self._on_final: Callable[[TranscriptResult], None] | None = None
        self._connection = None

    def on_interim(self, callback: Callable[[TranscriptResult], None]) -> None:
        self._on_interim = callback

    def on_final(self, callback: Callable[[TranscriptResult], None]) -> None:
        self._on_final = callback

    async def start(self) -> None:
        options = build_streaming_options(
            language=self.language,
            model=self.model,
            punctuate=True,
            interim_results=True,
        )

        async def on_transcript(data):
            payload = data.__dict__ if hasattr(data, "__dict__") else {}
            if "is_final" not in payload and "channel" not in payload:
                return
            result = normalize_deepgram_result(payload)
            if result.is_final:
                self._final_results.append(result)
                if self._on_final:
                    self._on_final(result)
            else:
                self._interim_buffer.append(result)
                if self._on_interim:
                    self._on_interim(result)

        self._connection = self.client.listen.asyncwebsocket.v("1")
        await self._connection.start(
            options=options,
            event_handler={
                LiveTranscriptionEvents.Transcript: on_transcript,
            },
        )
        logger.info(
            "PartialResultsHandler started with Deepgram model %s", options.get("model")
        )

    async def send_audio(self, pcm_bytes: bytes) -> None:
        if self._connection:
            await self._connection.send(pcm_bytes)

    async def finalize(self) -> None:
        if self._connection:
            await self._connection.finalize()
            await asyncio.sleep(0.5)
            await self._connection.finish()

    @property
    def interim_results(self) -> list[TranscriptResult]:
        return list(self._interim_buffer)

    @property
    def final_results(self) -> list[TranscriptResult]:
        return list(self._final_results)

    def get_merged_final_text(self) -> str:
        return " ".join(r.text.strip() for r in self._final_results if r.text.strip())

    def get_latest_interim_text(self) -> str:
        if self._interim_buffer:
            return self._interim_buffer[-1].text.strip()
        return ""


async def handle_streaming_events(
    audio_source: AsyncGenerator[bytes, None],
    language: str | None = None,
    model: str | None = None,
    client: DeepgramClient | None = None,
) -> AsyncGenerator[StreamingEvent, None]:
    handler = PartialResultsHandler(client=client, language=language, model=model)
    await handler.start()

    queue: asyncio.Queue[StreamingEvent | None] = asyncio.Queue()

    def on_final_cb(result: TranscriptResult):
        asyncio.get_event_loop().call_soon_threadsafe(
            queue.put_nowait,
            StreamingEvent(event_type="final", result=result),
        )

    def on_interim_cb(result: TranscriptResult):
        asyncio.get_event_loop().call_soon_threadsafe(
            queue.put_nowait,
            StreamingEvent(event_type="interim", result=result),
        )

    handler.on_final(on_final_cb)
    handler.on_interim(on_interim_cb)

    try:
        async for pcm_bytes in audio_source:
            await handler.send_audio(pcm_bytes)
            while not queue.empty():
                item = await queue.get()
                if item is None:
                    return
                yield item
            await asyncio.sleep(0.01)

        await handler.finalize()

        while not queue.empty():
            item = await queue.get()
            if item is None:
                return
            yield item
    except asyncio.CancelledError:
        await handler.finalize()
        raise
