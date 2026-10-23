import asyncio
import os
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
from typing import AsyncGenerator
from speech_client import DEEPGRAM_API_KEY


async def stream_chunks(
    audio_source: AsyncGenerator[bytes, None],
) -> AsyncGenerator[str, None]:
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY not set")

    client = DeepgramClient(DEEPGRAM_API_KEY)
    connection = client.listen.live.v("1")

    result_queue = asyncio.Queue()

    def transcript_callback(result, **kwargs):
        transcript = ""
        if (
            hasattr(result, "channel")
            and result.channel
            and result.channel.alternatives
        ):
            transcript = result.channel.alternatives[0].transcript.strip()
        is_final = getattr(result, "is_final", False)
        result_queue.put_nowait({"transcript": transcript, "is_final": is_final})

    connection.on(LiveTranscriptionEvents.Transcript, transcript_callback)

    await connection.start(
        LiveOptions(model="nova-2", language="en", smart_format=True, punctuate=True)
    )

    try:
        async for data in audio_source:
            connection.send(data)

            while True:
                try:
                    res = result_queue.get_nowait()
                    yield res["transcript"]
                except asyncio.QueueEmpty:
                    break
            await asyncio.sleep(0)
    finally:
        await connection.finish()
