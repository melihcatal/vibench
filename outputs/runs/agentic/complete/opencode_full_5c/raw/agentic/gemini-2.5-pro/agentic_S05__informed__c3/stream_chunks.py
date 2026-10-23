import asyncio
from typing import AsyncGenerator, Dict, Any

from deepgram import (
    LiveTranscriptionEvents,
    LiveOptions,
)

from speech_client import get_speech_client
from speech_models import StreamingTranscript


async def mock_audio_source() -> AsyncGenerator[bytes, None]:
    # In a real scenario, this would be a stream of audio chunks
    # from a file, a network stream, etc.
    for i in range(10):
        yield b"\x00" * 3200
        await asyncio.sleep(0.1)


async def stream_audio_chunks(
    audio_source: AsyncGenerator[bytes, None],
) -> AsyncGenerator[StreamingTranscript, None]:
    client = get_speech_client()
    dg_connection = client.listen.asynclive.v("1")

    results_queue = asyncio.Queue()

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if not sentence:
            return

        is_final = result.is_final
        confidence = result.channel.alternatives[0].confidence

        await results_queue.put(
            StreamingTranscript(
                text=sentence,
                is_final=is_final,
                confidence=confidence,
                words=result.channel.alternatives[0].words,
            )
        )

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
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
