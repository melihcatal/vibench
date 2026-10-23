import asyncio
from typing import AsyncGenerator, AsyncIterable

from deepgram import LiveTranscriptionEvents, LiveOptions, ResultResponse
from speech_client import get_deepgram_client

async def stream_with_language_settings(
    audio_source: AsyncIterable[bytes],
) -> AsyncGenerator[str, None]:
    """
    Starts a streaming recognizer with Spanish language and punctuation settings.
    """
    client = get_deepgram_client()
    dg_connection = client.listen.asynclive.v("1")

    transcript_queue = asyncio.Queue()

    async def on_message(self, result: ResultResponse, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            await transcript_queue.put(transcript)

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    
    # Configure Deepgram for Spanish language and punctuation
    options = LiveOptions(
        model="nova-2",
        language="es",
        punctuate=True,
    )
    await dg_connection.start(options)

    async def sender(dg_conn, source):
        async for chunk in source:
            await dg_conn.send(chunk)
        await dg_conn.finish()

    sender_task = asyncio.create_task(sender(dg_connection, audio_source))

    while not sender_task.done() or not transcript_queue.empty():
        try:
            transcript = await asyncio.wait_for(transcript_queue.get(), timeout=1.0)
            yield transcript
        except asyncio.TimeoutError:
            if sender_task.done():
                break
    
    await sender_task
