import asyncio
import threading
import pyaudio
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents
from speech_client import get_stt_client, get_live_options
from speech_models import STTConfig
from partial_results import TranscriptQueueHandler


async def stream_microphone() -> AsyncGenerator[str, None]:
    client = get_stt_client()
    options = get_live_options()
    queue: asyncio.Queue = asyncio.Queue()

    def on_close(_):
        queue.put_nowait(None)

    connection = (
        client.listen.live.v("1")
        .registerCallback(
            LiveTranscriptionEvents.Transcript, TranscriptQueueHandler(queue)
        )
        .registerCallback(LiveTranscriptionEvents.Close, on_close)
    )
    await connection.start(options)
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )

    def capture_audio():
        try:
            while True:
                frame = audio_stream.read(1024, exception_on_overflow=False)
                connection.send(frame)
        except:
            pass
        finally:
            audio_stream.stop_stream()
            audio_stream.close()
            pa.terminate()
            asyncio.get_event_loop().call_soon_threadsafe(
                lambda: queue.put_nowait(None)
            )

    mic_thread = threading.Thread(target=capture_audio, daemon=True)
    mic_thread.start()
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            transcript = item["transcript"].strip()
            marker = "" if item["is_final"] else "[partial] "
            yield marker + transcript
    finally:
        mic_thread.join(timeout=1.0)
        await connection.finish()
