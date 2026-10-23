import asyncio
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents
from speech_client import get_speech_client
from speech_models import (
    RecognizeConfig,
    deepgram_live_options,
    TranscriptChunk,
    parse_deepgram_transcript,
)


async def stream_chunks(
    audio_generator: AsyncGenerator[bytes, None],
    config: RecognizeConfig = RecognizeConfig(),
) -> AsyncGenerator[TranscriptChunk, None]:
    client = get_speech_client()
    connection = client.listen.live.v("1")
    transcript_queue: asyncio.Queue[TranscriptChunk | None] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def transcript_callback(result: dict):
        chunk = parse_deepgram_transcript(result)
        loop.call_soon_threadsafe(transcript_queue.put_nowait, chunk)

    def close_callback(_):
        loop.call_soon_threadsafe(transcript_queue.put_nowait, None)

    connection.on(LiveTranscriptionEvents.Transcript, transcript_callback)
    connection.on(LiveTranscriptionEvents.Close, close_callback)
    await connection.start(deepgram_live_options(config))

    try:
        async for audio_chunk in audio_generator:
            await connection.send(audio_chunk)
        await connection.finish()
        while True:
            chunk = await transcript_queue.get()
            if chunk is None:
                break
            yield chunk
    except:
        await connection.finish()
        while True:
            chunk = await transcript_queue.get()
            if chunk is None:
                break
            yield chunk
