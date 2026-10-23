import asyncio
from typing import AsyncGenerator
import pyaudio
from deepgram.core.events import EventType
from speech_client import get_async_stt_client
from speech_models import LiveSTTConfig

async def stream_transcripts(config: LiveSTTConfig = LiveSTTConfig()) -> AsyncGenerator[str, None]:
    client = get_async_stt_client()
    queue = asyncio.Queue()

    def on_message(message):
        if message.type == 'Transcript' and message.channel and message.channel.alternatives:
            alternative = message.channel.alternatives[0]
            text = alternative.transcript.strip()
            if text:
                is_final = getattr(message, 'is_final', False)
                status = 'final' if is_final else 'interim'
                queue.put_nowait(f&quot;[{status}] {text}&quot;)

    p = pyaudio.PyAudio()
    stream = None
    try:
        stream = p.open(
            format=pyaudio.paInt16,
            channels=config.channels,
            rate=config.sample_rate,
            input=True,
            frames_per_buffer=1024,
        )
        async with client.listen.v2.connect(
            model=config.model,
            language=config.language,
            punctuate=config.punctuate,
            interim_results=config.interim_results,
            channels=config.channels,
            sample_rate=config.sample_rate,
            encoding=config.encoding,
        ) as connection:
            connection.on(EventType.MESSAGE, on_message)
            await connection.start_listening()
            audio_task = asyncio.create_task(send_audio_loop(stream, connection))
            try:
                while True:
                    event = await queue.get()
                    yield event
            finally:
                audio_task.cancel()
    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        p.terminate()

async def send_audio_loop(stream, connection):
    while True:
        data = await asyncio.to_thread(stream.read, 1024, exception_on_overflow=False)
        await asyncio.to_thread(connection.send, data)
