"""Streams audio chunks from an async source using Deepgram Streaming Speech-to-Text."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterable
from typing import Any, AsyncIterator, Callable

from deepgram import DeepgramClient, LiveOptions

from speech_client import create_deepgram_client, build_live_options
from speech_models import (
    PartialTranscript,
    FinalTranscript,
    normalize_deepgram_interim,
    normalize_deepgram_final,
)


async def stream_chunks(
    audio_source: AsyncIterable[bytes],
    model: str = "nova-2",
    language: str = "en",
    sample_rate: int = 16000,
    channels: int = 1,
    interim_results: bool = True,
    punctuate: bool = True,
    smart_format: bool = True,
    on_interim: Callable[[PartialTranscript], None] | None = None,
    on_final: Callable[[FinalTranscript], None] | None = None,
    **extra_options: Any,
) -> AsyncIterator[PartialTranscript | FinalTranscript]:
    """
    Stream audio chunks from an async source to Deepgram and yield transcripts.

    Parameters
    ----------
    audio_source : AsyncIterable[bytes]
        An async iterable yielding raw PCM audio chunks.
    model : str
        Deepgram model identifier (e.g. "nova-2", "enhanced", "base").
    language : str
        Language code for recognition.
    sample_rate : int
        Audio sample rate in Hz.
    channels : int
        Number of audio channels.
    interim_results : bool
        Whether to receive interim (partial) results.
    punctuate : bool
        Whether to enable automatic punctuation.
    smart_format : bool
        Whether to apply smart formatting to transcripts.
    on_interim / on_final : callback
        Optional callbacks invoked for each interim/final transcript.
    """
    client = create_deepgram_client()
    options = build_live_options(
        model=model,
        language=language,
        sample_rate=sample_rate,
        channels=channels,
        interim_results=interim_results,
        punctuate=punctuate,
        smart_format=smart_format,
        **extra_options,
    )

    async with client.listen.async_live.v("1").stream(options) as stream:
        async for chunk in audio_source:
            await stream.send(chunk)

        await stream.send({"type": "CloseStream"})

        async for result in stream:
            if result.is_final:
                transcript = normalize_deepgram_final(result)
                if on_final:
                    on_final(transcript)
                yield transcript
            else:
                transcript = normalize_deepgram_interim(result)
                if on_interim:
                    on_interim(transcript)
                yield transcript
