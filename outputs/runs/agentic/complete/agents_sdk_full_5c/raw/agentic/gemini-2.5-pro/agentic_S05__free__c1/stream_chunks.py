import asyncio
from typing import AsyncGenerator, AsyncIterable, Optional
from deepgram import LiveTranscriptionEvents, LiveOptions, ResultResponse

from speech_client import get_deepgram_client
from speech_models import StreamingTranscript

async def _mock_audio_chunk_source() -> AsyncGenerator[bytes, None]:
    """A mock async generator for audio chunks."""
    # In a real scenario, this could be a stream from a file, network, etc.
    for i in range(5):
        yield b'\x00' * 4096  # Yielding silent audio chunks
        await asyncio.sleep(0.5)

async def stream_transcription_from_chunks(
    audio_source: Optional[AsyncIterable[bytes]] = None,
) -> AsyncGenerator[StreamingTranscript, None]:
    """
    Connects to Deepgram and streams audio chunks from an async source,
    yielding transcript results.
    """
    if audio_source is None:
        audio_source = _mock_audio_chunk_source()

    client = get_deepgram_client()
    dg_connection = client.listen.asynclive.v("1")

    transcript_queue = asyncio.Queue()

    async def on_message(self, result: ResultResponse, **kwargs):
        if result.channel and result.channel.alternatives:
            transcript_model = StreamingTranscript(
                is_final=result.is_final,
                speech_final=result.speech_final,
                start=result.start,
                duration=result.duration,
                channel=result.channel
            )
            await transcript_queue.put(transcript_model)

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(model="nova-2", language="en-US")
    await dg_connection.start(options)

    async def sender(dg_conn, source):
        async for chunk in source:
            await dg_conn.send(chunk)
        await dg_conn.finish()

    sender_task = asyncio.create_task(sender(dg_connection, audio_source))
    
    while not sender_task.done() or not transcript_queue.empty():
        try:
            transcript = await asyncio.wait_for(transcript_queue.get(), timeout=1.0)
            yield transcript
        except asyncio.TimeoutError:
            if sender_task.done():
                break

    await sender_task

