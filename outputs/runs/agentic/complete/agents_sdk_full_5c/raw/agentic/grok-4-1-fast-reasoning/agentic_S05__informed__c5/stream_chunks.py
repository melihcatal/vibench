import asyncio
from typing import AsyncGenerator, AsyncIterable
from deepgram import LiveTranscriptionEvents
from speech_client import get_speech_client
from speech_models import get_live_options

async def stream_audio_chunks(audio_chunks: AsyncIterable[bytes]) -> AsyncGenerator[str, None]:
    client = get_speech_client()
    options = get_live_options()
    transcript_queue = asyncio.Queue()
    connection = client.listen.live.v("1", options)

    def on_transcript(result):
        try:
            transcript = result.channel.alternatives[0].transcript.strip()
            if transcript:
                loop = asyncio.get_event_loop()
                loop.call_soon_threadsafe(transcript_queue.put_nowait, transcript)
        except Exception:
            pass

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    connection.start()

    async def sender():
        async for chunk in audio_chunks:
            connection.send(chunk)

    sender_task = asyncio.create_task(sender())

    try:
        while True:
            yield await transcript_queue.get()
    finally:
        sender_task.cancel()
        try:
            await sender_task
        except asyncio.CancelledError:
            pass
        connection.finish()
