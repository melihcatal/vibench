import asyncio
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents, LiveOptions
from speech_client import get_speech_client
from speech_models import Caption


async def stream_audio_chunks(async_audio_source: AsyncGenerator[bytes, None]):
    """Streams audio chunks from an async source and yields transcripts."""
    transcript_queue = asyncio.Queue()
    client = get_speech_client()
    dg_connection = client.listen.live.v("1")

    async def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if len(transcript) > 0:
            await transcript_queue.put(
                Caption(text=transcript, is_final=result.is_final)
            )

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(model="nova-2", language="en-US")
    await dg_connection.start(options)

    async def sender(connection):
        async for chunk in async_audio_source:
            connection.send(chunk)
        await connection.finish()

    sender_task = asyncio.create_task(sender(dg_connection))

    try:
        while not sender_task.done():
            try:
                yield await asyncio.wait_for(transcript_queue.get(), timeout=1)
            except asyncio.TimeoutError:
                pass
    finally:
        await sender_task
