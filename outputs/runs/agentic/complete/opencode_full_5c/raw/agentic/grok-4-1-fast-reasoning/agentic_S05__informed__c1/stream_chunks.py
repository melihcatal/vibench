import asyncio
from typing import AsyncGenerator, AsyncIterable
from speech_client import dg_client
from speech_models import TranscriptChunk
from deepgram import LiveOptions, LiveTranscriptionEvents
from deepgram.types.live import LiveTranscriptResult


async def stream_chunks(
    audio_chunks: AsyncIterable[bytes],
) -> AsyncGenerator[TranscriptChunk, None]:
    trans_queue: asyncio.Queue[TranscriptChunk] = asyncio.Queue()

    def transcript_handler(transcript: LiveTranscriptResult):
        if transcript.channel and transcript.channel.alternatives:
            text = transcript.channel.alternatives[0].transcript or ""
            is_final = transcript.is_final
            trans_queue.put_nowait(TranscriptChunk(text=text, is_final=is_final))

    connection = dg_client.listen.live.v("1")
    connection.on(LiveTranscriptionEvents.Transcript, transcript_handler)

    options = LiveOptions(
        model="nova-2",
        sample_rate=16000,
        channels=1,
        interim_results=True,
        language="en",
        punctuate=True,
    )

    async def send_audio():
        try:
            async for chunk in audio_chunks:
                connection.send(chunk)
        except Exception:
            pass

    await connection.start(options)
    send_task = asyncio.create_task(send_audio())

    try:
        while True:
            chunk = await trans_queue.get()
            yield chunk
    finally:
        send_task.cancel()
        await send_task
        await connection.finish()
        # Drain remaining transcripts
        while True:
            try:
                chunk = trans_queue.get_nowait()
                yield chunk
            except asyncio.QueueEmpty:
                break
