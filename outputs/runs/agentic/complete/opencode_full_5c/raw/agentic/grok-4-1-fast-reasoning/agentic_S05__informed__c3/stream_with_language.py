import asyncio
from typing import AsyncGenerator
from deepgram import LiveOptions, LiveTranscriptionEvents
from deepgram.utils.microphone import Microphone
from speech_client import get_speech_client
from speech_models import get_transcript_info


async def stream_microphone_transcripts_with_language(
    language: str = "en", punctuate: bool = True
) -> AsyncGenerator[str, None]:
    client = get_speech_client()
    options = LiveOptions(
        language=language,
        punctuate=punctuate,
        model="nova-2",
        smart_format=True,
    )
    connection = client.listen.live.v("1", options)
    queue: asyncio.Queue[str | None] = asyncio.Queue()

    def on_transcript(result, **kwargs):
        transcript, _ = get_transcript_info(result)
        if transcript:
            queue.put_nowait(transcript)

    def on_close(*args):
        queue.put_nowait(None)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    connection.on(LiveTranscriptionEvents.Close, on_close)
    connection.start()
    microphone = Microphone()

    async def send_audio():
        try:
            async for buffer in microphone.read_chunks():
                connection.send(buffer)
        except:
            pass
        finally:
            connection.finish()

    send_task = asyncio.create_task(send_audio())
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        send_task.cancel()
        try:
            await send_task
        except asyncio.CancelledError:
            pass
