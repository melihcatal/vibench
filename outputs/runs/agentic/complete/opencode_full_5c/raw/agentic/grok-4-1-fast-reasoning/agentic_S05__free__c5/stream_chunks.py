import asyncio
from typing import AsyncGenerator, AsyncIterable
from deepgram import LiveTranscriptionEvents
from speech_client import get_stt_client, get_live_options
from partial_results import TranscriptQueueHandler


async def stream_chunks(
    audio_source: AsyncIterable[bytes],
) -> AsyncGenerator[str, None]:
    client = get_stt_client()
    options = get_live_options()
    queue: asyncio.Queue = asyncio.Queue()

    def on_close(_):
        queue.put_nowait(None)

    connection = (
        client.listen.live.v("1")
        .registerCallback(
            LiveTranscriptionEvents.Transcript, TranscriptQueueHandler(queue)
        )
        .registerCallback(LiveTranscriptionEvents.Close, on_close)
    )
    await connection.start(options)

    async def send_audio():
        try:
            async for chunk in audio_source:
                connection.send(chunk)
        finally:
            await connection.finish()

    sender_task = asyncio.create_task(send_audio())
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            transcript = item["transcript"].strip()
            marker = "" if item["is_final"] else "[partial] "
            yield marker + transcript
    finally:
        if not sender_task.done():
            sender_task.cancel()
        await asyncio.gather(sender_task, return_exceptions=True)
