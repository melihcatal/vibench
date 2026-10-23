import asyncio
from typing import AsyncGenerator

from deepgram import (
    LiveTranscriptionEvents,
    LiveOptions,
)

from speech_client import get_speech_client
from speech_models import StreamingTranscript


async def handle_partial_and_final_results(
    audio_source: AsyncGenerator[bytes, None],
) -> AsyncGenerator[StreamingTranscript, None]:
    client = get_speech_client()
    dg_connection = client.listen.asynclive.v("1")

    results_queue = asyncio.Queue()

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if not sentence:
            return

        transcript = StreamingTranscript(
            text=sentence,
            is_final=result.is_final,
            confidence=result.channel.alternatives[0].confidence,
        )
        await results_queue.put(transcript)

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        interim_results=True,
        utterance_end_ms="1000",
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
            if result.is_final:
                # Potentially trigger actions on final transcripts
                pass
        except asyncio.TimeoutError:
            if sender_task.done():
                break

    await sender_task
