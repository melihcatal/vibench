import asyncio
import pyaudio
import threading
from typing import AsyncGenerator
import os
from deepgram import LiveTranscriptionEvents
from speech_client import get_speech_client
from speech_models import (
    RecognizeConfig,
    deepgram_live_options,
    TranscriptChunk,
    parse_deepgram_transcript,
)


async def stream_microphone(
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

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1600,
    )

    def mic_loop():
        while True:
            audio_data = stream.read(1600, exception_on_overflow=False)
            future = asyncio.run_coroutine_threadsafe(connection.send(audio_data), loop)
            try:
                future.result(timeout=1)
            except:
                break

    mic_thread = threading.Thread(target=mic_loop, daemon=True)
    mic_thread.start()

    try:
        while True:
            chunk = await transcript_queue.get()
            if chunk is None:
                break
            yield chunk
    finally:
        await connection.finish()
        stream.stop_stream()
        stream.close()
        p.terminate()
