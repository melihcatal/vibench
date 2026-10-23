import asyncio
from typing import AsyncGenerator, Any
from deepgram import DeepgramClient
from deepgram.types import LiveOptions, LiveTranscriptionEvents
from speech_client import DEEPGRAM_API_KEY


async def partial_results(
    audio_chunks: AsyncGenerator[bytes, None],
) -> AsyncGenerator[str, None]:
    client = DeepgramClient(DEEPGRAM_API_KEY)
    options = LiveOptions(
        model="nova-2-general",
        language="en-US",
        punctuate=True,
        interim_results=True,
        smart_format=True,
    )
    live = client.listen.live.v("1", options)
    transcript_queue: asyncio.Queue[str] = asyncio.Queue()
    audio_queue: asyncio.Queue[bytes] = asyncio.Queue()
    closed = False
    partial_buffer = ""

    def on_transcript(result: Any, **kwargs):
        nonlocal partial_buffer
        if result.channel and result.channel.alternatives:
            text = result.channel.alternatives[0].transcript or ""
        else:
            text = ""
        if result.is_final:
            final_text = (partial_buffer + " " + text).strip()
            transcript_queue.put_nowait(final_text)
            partial_buffer = ""
        else:
            partial_buffer += text + " "

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
                text = await asyncio.wait_for(transcript_queue.get(), timeout=1.0)
                yield text
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
