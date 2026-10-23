import asyncio
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents
from speech_client import get_stt_client
from speech_models import StreamingConfig, create_live_options

async def stream_chunks(audio_chunks: AsyncGenerator[bytes, None], config: StreamingConfig = StreamingConfig()) -> AsyncGenerator[tuple[str, str], None]:
    client = get_stt_client()
    connection = client.listen.live.v(config.version)
    options = create_live_options(config)
    transcript_queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def on_transcript(result, **_):
        alt = result.channel.alternatives[0]
        text = alt.transcript or ""
        typ = "final" if result.speech_final else "interim"
        asyncio.run_coroutine_threadsafe(transcript_queue.put((typ, text)), loop)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    await connection.start(options)

    try:
        send_task = asyncio.create_task(send_audio(connection, audio_chunks))
        while True:
            typ, text = await asyncio.wait_for(transcript_queue.get(), timeout=1.0)
            yield typ, text
    except asyncio.CancelledError:
        pass
    finally:
        send_task.cancel()
        await connection.finish()

async def send_audio(connection, audio_chunks: AsyncGenerator[bytes, None]):
    async for chunk in audio_chunks:
        connection.send(chunk)
