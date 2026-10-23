import asyncio
from typing import AsyncIterator
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from speech_client import client
from speech_models import (
    TranscriptChunk,
    LiveOptions,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
)


async def stream_chunks(
    audio_stream: AsyncIterator[bytes], options: LiveOptions = None
) -> AsyncIterator[TranscriptChunk]:
    if options is None:
        options = {}
    transcript_queue = asyncio.Queue()

    def on_message(message):
        if message.type == "Transcript":
            alt = message.channel.alternatives[0]
            chunk: TranscriptChunk = {
                "transcript": alt.transcript,
                "is_final": message.is_final,
                "confidence": alt.confidence,
            }
            asyncio.get_running_loop().call_soon(
                lambda: asyncio.create_task(transcript_queue.put(chunk))
            )

    connection = client.listen.v2.connect(
        model=options.get("model", "nova-2"),
        sample_rate=AUDIO_SAMPLE_RATE,
        channels=AUDIO_CHANNELS,
        encoding="linear16",
        language=options.get("language", "en"),
        punctuate=options.get("punctuate", True),
        interim_results=options.get("interim_results", True),
    )

    connection.on(EventType.MESSAGE, on_message)

    async with connection:
        connection.start_listening()
        send_task = asyncio.create_task(send_audio_chunks(audio_stream, connection))
        try:
            while True:
                chunk = await transcript_queue.get()
                yield chunk
        finally:
            send_task.cancel()


async def send_audio_chunks(audio_stream: AsyncIterator[bytes], connection):
    async for chunk in audio_stream:
        connection.send(chunk)
