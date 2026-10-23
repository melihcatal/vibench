import asyncio
from typing import AsyncIterator, Optional, List

from speech_client import create_deepgram_client, StreamConfig
from speech_models import (
    StreamingSpeechEvent,
    StreamingRecognitionResult,
    SpeechEventType,
    build_streaming_request,
)
from partial_results import PartialResultHandler


def create_language_config(
    language: str = "en-US",
    model: str = "nova-2",
    punctuate: bool = True,
    profanity_filter: bool = False,
    smart_format: bool = True,
    interim_results: bool = True,
    sample_rate: int = 16000,
    channels: int = 1,
    encoding: str = "linear16",
    vad_events: bool = True,
    endpointing: Optional[int] = None,
    extra_options: Optional[dict] = None,
) -> StreamConfig:
    return StreamConfig(
        model=model,
        language=language,
        punctuate=punctuate,
        profanity_filter=profanity_filter,
        smart_format=smart_format,
        interim_results=interim_results,
        sample_rate=sample_rate,
        channels=channels,
        encoding=encoding,
        vad_events=vad_events,
        endpointing=endpointing,
        extra=extra_options or {},
    )


async def start_streaming_recognizer(
    audio_source: AsyncIterator[bytes],
    language: str = "en-US",
    punctuate: bool = True,
    model: str = "nova-2",
    profanity_filter: bool = False,
    smart_format: bool = True,
    interim_results: bool = True,
    sample_rate: int = 16000,
    channels: int = 1,
    encoding: str = "linear16",
    vad_events: bool = True,
    endpointing: Optional[int] = None,
    extra_options: Optional[dict] = None,
    on_interim: Optional[callable] = None,
    on_final: Optional[callable] = None,
) -> AsyncIterator[StreamingRecognitionResult]:
    config = create_language_config(
        language=language,
        model=model,
        punctuate=punctuate,
        profanity_filter=profanity_filter,
        smart_format=smart_format,
        interim_results=interim_results,
        sample_rate=sample_rate,
        channels=channels,
        encoding=encoding,
        vad_events=vad_events,
        endpointing=endpointing,
        extra_options=extra_options,
    )

    options = build_streaming_request(
        language=language,
        model=model,
        punctuate=punctuate,
        profanity_filter=profanity_filter,
        smart_format=smart_format,
        interim_results=interim_results,
        sample_rate=sample_rate,
        channels=channels,
        encoding=encoding,
        vad_events=vad_events,
        endpointing=endpointing,
        extra_options=extra_options,
    )

    client = create_deepgram_client()
    dg_connection = client.listen.live.v("1")

    handler = PartialResultHandler(
        on_interim=on_interim,
        on_final=on_final,
    )

    async def send_audio():
        try:
            async for chunk in audio_source:
                dg_connection.send(chunk)
                await asyncio.sleep(0)
        except Exception:
            pass

    send_task = asyncio.create_task(send_audio())

    try:
        async for result in dg_connection:
            event = StreamingSpeechEvent.from_deepgram_event(result)
            recognition_result = handler.handle_event(event)
            if recognition_result is not None:
                yield recognition_result
    finally:
        send_task.cancel()
        try:
            await send_task
        except asyncio.CancelledError:
            pass
        dg_connection.finish()


async def stream_with_punctuation(
    audio_source: AsyncIterator[bytes],
    language: str = "en-US",
    punctuate: bool = True,
    profanity_filter: bool = False,
) -> AsyncIterator[StreamingRecognitionResult]:
    async for result in start_streaming_recognizer(
        audio_source=audio_source,
        language=language,
        punctuate=punctuate,
        profanity_filter=profanity_filter,
    ):
        yield result


async def stream_multilingual(
    audio_source: AsyncIterator[bytes],
    languages: List[str],
    punctuate: bool = True,
) -> AsyncIterator[StreamingRecognitionResult]:
    primary_language = languages[0] if languages else "en-US"
    extra = {"multilingual": True, "detect_language": True, "languages": languages}

    async for result in start_streaming_recognizer(
        audio_source=audio_source,
        language=primary_language,
        punctuate=punctuate,
        extra_options=extra,
    ):
        yield result
