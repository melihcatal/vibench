import asyncio
import pyaudio
from typing import AsyncGenerator
from deepgram import LiveOptions, LiveTranscriptionEvents
from speech_client import get_dg_client
from speech_models import Transcript


async def stream_with_language(
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
    SAMPLE_RATE = 16000
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    CHUNK = 480

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
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
            while not end_event.is_set():
                data = stream.read(CHUNK, exception_on_overflow=False)
                await connection.send(data)
                await asyncio.sleep(0)
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
        stream.stop_stream()
        stream.close()
        p.terminate()
        await connection.finish()
