import asyncio
from typing import AsyncGenerator, Tuple, AsyncIterable

from deepgram import LiveTranscriptionEvents, LiveOptions, ResultResponse

from speech_client import get_deepgram_client

async def handle_partial_and_final_results(
    audio_source: AsyncIterable[bytes],
) -> AsyncGenerator[Tuple[str, bool], None]:
    """
    Handles partial and final streaming recognition events from Deepgram.
    Yields a tuple of (transcript, is_final_flag).
    """
    client = get_deepgram_client()
    dg_connection = client.listen.asynclive.v("1")

    result_queue = asyncio.Queue()

    async def on_message(self, result: ResultResponse, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            await result_queue.put((transcript, result.is_final))

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    
    options = LiveOptions(
        model="nova-2",
        language="en-US",
        interim_results=True
    )
    await dg_connection.start(options)

    async def sender(dg_conn, source):
        async for chunk in source:
            await dg_conn.send(chunk)
        await dg_conn.finish()

    sender_task = asyncio.create_task(sender(dg_connection, audio_source))

    while not sender_task.done() or not result_queue.empty():
        try:
            transcript, is_final = await asyncio.wait_for(result_queue.get(), timeout=1.0)
            yield transcript, is_final
        except asyncio.TimeoutError:
            if sender_task.done():
                break

    await sender_task
