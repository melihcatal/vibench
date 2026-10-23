"""Handles partial and final streaming recognition events using Deepgram Streaming Speech-to-Text."""

from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Callable, Deque

from deepgram import DeepgramClient, LiveOptions

from speech_client import create_deepgram_client, build_live_options
from speech_models import (
    PartialTranscript,
    FinalTranscript,
    normalize_deepgram_interim,
    normalize_deepgram_final,
    aggregate_transcripts,
)


@dataclass
class RecognitionSession:
    """Tracks the state of an ongoing streaming recognition session."""
    interim_buffer: Deque[PartialTranscript] = field(default_factory=deque)
    final_results: list[FinalTranscript] = field(default_factory=list)
    total_interim_count: int = 0
    total_final_count: int = 0
    current_interim_text: str = ""

    def on_interim(self, partial: PartialTranscript) -> None:
        """Handle a new interim result, replacing the current interim text."""
        self.interim_buffer.append(partial)
        self.total_interim_count += 1
        self.current_interim_text = partial.text

    def on_final(self, final: FinalTranscript) -> None:
        """Handle a final result, clearing the interim buffer for that segment."""
        self.final_results.append(final)
        self.total_final_count += 1
        self.current_interim_text = ""

    def get_aggregated_text(self) -> str:
        """Return all final transcripts plus the latest interim text."""
        segments: list[str] = [r.text for r in self.final_results]
        if self.current_interim_text:
            segments.append(self.current_interim_text)
        return " ".join(segments).strip()


async def process_streaming_events(
    audio_chunks: AsyncIterator[bytes],
    model: str = "nova-2",
    language: str = "en",
    sample_rate: int = 16000,
    channels: int = 1,
    interim_results: bool = True,
    punctuate: bool = True,
    on_interim: Callable[[RecognitionSession, PartialTranscript], None] | None = None,
    on_final: Callable[[RecognitionSession, FinalTranscript], None] | None = None,
) -> AsyncIterator[RecognitionSession]:
    """
    Process Deepgram streaming events, maintaining session state.

    Yields a RecognitionSession snapshot after each event (interim or final).
    """
    client = create_deepgram_client()
    options = build_live_options(
        model=model,
        language=language,
        sample_rate=sample_rate,
        channels=channels,
        interim_results=interim_results,
        punctuate=punctuate,
    )

    session = RecognitionSession()

    async with client.listen.async_live.v("1").stream(options) as stream:
        async def chunk_sender():
            async for chunk in audio_chunks:
                await stream.send(chunk)
            await stream.send({"type": "CloseStream"})

        sender_task = asyncio.create_task(chunk_sender())

        try:
            async for result in stream:
                if result.is_final:
                    transcript = normalize_deepgram_final(result)
                    session.on_final(transcript)
                    if on_final:
                        on_final(session, transcript)
                else:
                    transcript = normalize_deepgram_interim(result)
                    session.on_interim(transcript)
                    if on_interim:
                        on_interim(session, transcript)

                yield session

        finally:
            sender_task.cancel()
            try:
                await sender_task
            except asyncio.CancelledError:
                pass
