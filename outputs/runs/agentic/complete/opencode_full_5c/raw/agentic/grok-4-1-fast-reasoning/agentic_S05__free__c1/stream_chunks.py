import asyncio
from typing import AsyncGenerator, AsyncIterable
from deepgram import LiveTranscriptionEvents, LiveOptions
from deepgram.utils.offset_types import LiveOffsetData
from speech_client import get_dg_client
from speech_models import Transcript


async def stream_chunks(
    audio_chunks: AsyncIterable[bytes],
    language_code: str = "en-US",
    punctuate: bool = True,
) -> AsyncGenerator[Transcript, None]:
    client = get_dg_client()
    options = LiveOptions(
        model="nova-2",
        language=language_code,
        punctuate=punctuate,
        interim_results=True,
    )
    transcript_q = asyncio.Queue()
    end_event = asyncio.Event()
    connection = client.listen.live.v("1")

    @connection.on(LiveTranscriptionEvents.Open)
    async def on_open(_):
        pass

    @connection.on(LiveTranscriptionEvents.Transcript)
    async def on_transcript(data):
        if hasattr(data, "channel") and data.channel.alternatives:
            alt = data.channel.alternatives[0]
            t: Transcript = {
                "text": alt.transcript or "",
                "is_final": getattr(data.channel, "is_final", False),
                "confidence": getattr(alt, "confidence", None),
            }
            await transcript_q.put(t)

    @connection.on(LiveTranscriptionEvents.Close)
    async def on_close(_):
        await transcript_q.put(None)
        end_event.set()

    await connection.start(options)

    async def send_audio():
        try:
            async for chunk in audio_chunks:
                await connection.send(chunk)
            end_event.set()
        except:
            end_event.set()

    send_task = asyncio.create_task(send_audio())

    try:
        while True:
            item = await asyncio.wait_for(transcript_q.get(), timeout=30.0)
            if item is None:
                break
            yield item
    except asyncio.TimeoutError:
        pass
    finally:
        send_task.cancel()
        await connection.finish()
