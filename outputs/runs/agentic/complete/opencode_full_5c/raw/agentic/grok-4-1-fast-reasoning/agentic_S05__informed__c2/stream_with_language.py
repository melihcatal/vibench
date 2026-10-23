import asyncio
from typing import AsyncGenerator, Any
from deepgram import DeepgramClient
from deepgram.types import LiveOptions, LiveTranscriptionEvents
from speech_client import DEEPGRAM_API_KEY
from speech_models import TranscriptChunk


async def stream_with_language(
    audio_chunks: AsyncGenerator[bytes, None],
    language: str = "en-US",
    punctuate: bool = True,
) -> AsyncGenerator[TranscriptChunk, None]:
    client = DeepgramClient(DEEPGRAM_API_KEY)
    options = LiveOptions(
        model="nova-2-general",
        language=language,
        punctuate=punctuate,
        interim_results=True,
        smart_format=True,
    )
    live = client.listen.live.v("1", options)
    transcript_queue: asyncio.Queue[TranscriptChunk] = asyncio.Queue()
    audio_queue: asyncio.Queue[bytes] = asyncio.Queue()
    closed = False

    def on_transcript(result: Any, **kwargs):
        if result.channel and result.channel.alternatives:
            text = result.channel.alternatives[0].transcript or ""
        else:
            text = ""
        is_final = result.is_final
        transcript_queue.put_nowait(TranscriptChunk(text=text, is_final=is_final))

    def on_close(result: Any, **kwargs):
        nonlocal closed
        closed = True

    live.registerHandler(LiveTranscriptionEvents.Transcript, on_transcript)
    live.registerHandler(LiveTranscriptionEvents.Close, on_close)
    await live.hold()

    async def send_loop():
        nonlocal closed
        while not closed:
            try:
                chunk = await asyncio.wait_for(audio_queue.get(), timeout=0.5)
                live.send(chunk)
            except asyncio.TimeoutError:
                continue
            except:
                break

    send_task = asyncio.create_task(send_loop())

    async def feed_loop():
        async for chunk in audio_chunks:
            await audio_queue.put(chunk)
        nonlocal closed
        closed = True

    feed_task = asyncio.create_task(feed_loop())

    try:
        while not closed:
            try:
                chunk = await asyncio.wait_for(transcript_queue.get(), timeout=1.0)
                yield chunk
            except asyncio.TimeoutError:
                continue
    finally:
        closed = True
        feed_task.cancel()
        send_task.cancel()
        try:
            await live.finish()
        except:
            pass
