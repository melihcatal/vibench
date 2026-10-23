import asyncio
from typing import AsyncIterator, Optional

from speech_client import create_deepgram_client, StreamConfig
from speech_models import StreamingSpeechEvent, SpeechEventType


async def stream_audio_chunks(
    audio_source: AsyncIterator[bytes],
    config: Optional[StreamConfig] = None,
    chunk_size: int = 4096,
) -> AsyncIterator[StreamingSpeechEvent]:
    client = create_deepgram_client()
    cfg = config or StreamConfig()
    options = cfg.to_deepgram_options()

    dg_connection = client.listen.live.v("1")

    async def send_audio():
        async for chunk in audio_source:
            if len(chunk) > chunk_size:
                for i in range(0, len(chunk), chunk_size):
                    sub_chunk = chunk[i : i + chunk_size]
                    dg_connection.send(sub_chunk)
                    await asyncio.sleep(0)
            else:
                dg_connection.send(chunk)
                await asyncio.sleep(0)

    send_task = asyncio.create_task(send_audio())

    try:
        async for result in dg_connection:
            event = StreamingSpeechEvent.from_deepgram_event(result)
            if event.event_type == SpeechEventType.TRANSCRIPT and event.result:
                yield event
            elif event.event_type == SpeechEventType.SPEECH_ENDED:
                yield event
    finally:
        send_task.cancel()
        try:
            await send_task
        except asyncio.CancelledError:
            pass
        dg_connection.finish()


async def stream_bytes_chunks(
    byte_iterator: AsyncIterator[bytes],
    config: Optional[StreamConfig] = None,
) -> AsyncIterator[StreamingSpeechEvent]:
    async for event in stream_audio_chunks(byte_iterator, config):
        yield event
