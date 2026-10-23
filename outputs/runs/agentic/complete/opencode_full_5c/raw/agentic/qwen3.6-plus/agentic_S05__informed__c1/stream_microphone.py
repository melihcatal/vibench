import asyncio
from typing import AsyncIterator, Optional

import pyaudio

from speech_client import (
    create_deepgram_client,
    StreamConfig,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_CHANNELS,
)
from speech_models import (
    StreamingSpeechEvent,
    SpeechEventType,
    StreamingRecognitionResult,
)
from partial_results import PartialResultHandler


PYAUDIO_FORMAT = pyaudio.paInt16
BYTES_PER_SAMPLE = 2
CHUNK_DURATION_MS = 100
CHUNK_SIZE = int(DEFAULT_SAMPLE_RATE * BYTES_PER_SAMPLE * CHUNK_DURATION_MS / 1000)


def open_microphone_stream(
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    channels: int = DEFAULT_CHANNELS,
    chunk_size: int = CHUNK_SIZE,
):
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=PYAUDIO_FORMAT,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )
    return pa, stream


async def microphone_audio_generator(
    audio_stream,
    chunk_size: int = CHUNK_SIZE,
) -> AsyncIterator[bytes]:
    loop = asyncio.get_event_loop()
    while True:
        chunk = await loop.run_in_executor(None, audio_stream.read, chunk_size, False)
        yield chunk


async def stream_microphone_transcripts(
    config: Optional[StreamConfig] = None,
    on_interim: Optional[callable] = None,
    on_final: Optional[callable] = None,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    channels: int = DEFAULT_CHANNELS,
) -> AsyncIterator[StreamingRecognitionResult]:
    cfg = config or StreamConfig(
        sample_rate=sample_rate,
        channels=channels,
    )

    client = create_deepgram_client()
    dg_connection = client.listen.live.v("1")
    options = cfg.to_deepgram_options()

    dg_connection.start(options)

    pa, audio_stream = open_microphone_stream(
        sample_rate=sample_rate,
        channels=channels,
    )

    handler = PartialResultHandler(
        on_interim=on_interim,
        on_final=on_final,
    )

    async def send_audio():
        try:
            async for chunk in microphone_audio_generator(audio_stream):
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
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()


async def yield_interim_transcripts(
    config: Optional[StreamConfig] = None,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    channels: int = DEFAULT_CHANNELS,
) -> AsyncIterator[str]:
    async for result in stream_microphone_transcripts(
        config=config,
        sample_rate=sample_rate,
        channels=channels,
    ):
        if not result.is_final:
            yield result.text
