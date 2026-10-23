import asyncio
from typing import AsyncGenerator

from deepgram import (
    LiveTranscriptionEvents,
    LiveOptions,
)

from speech_client import get_speech_client
from speech_models import StreamingTranscript


async def stream_with_settings(
    audio_source: AsyncGenerator[bytes, None],
    language: str = "en-US",
    punctuate: bool = True,
) -> AsyncGenerator[StreamingTranscript, None]:
    client = get_speech_client()
    dg_connection = client.listen.asynclive.v("1")

    results_queue = asyncio.Queue()

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if not sentence:
            return

        await results_queue.put(
            StreamingTranscript(
                text=sentence,
                is_final=result.is_final,
                confidence=result.channel.alternatives[0].confidence,
            )
        )

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        language=language,
        punctuate=punctuate,
        interim_results=True,
    )
    await dg_connection.start(options)

    async def sender():
        async for chunk in audio_source:
            await dg_connection.send(chunk)
        await dg_connection.finish()

    sender_task = asyncio.create_task(sender())

    while not sender_task.done() or not results_queue.empty():
        try:
            result = await asyncio.wait_for(results_queue.get(), timeout=1.0)
            yield result
        except asyncio.TimeoutError:
            if sender_task.done():
                break

    await sender_task
