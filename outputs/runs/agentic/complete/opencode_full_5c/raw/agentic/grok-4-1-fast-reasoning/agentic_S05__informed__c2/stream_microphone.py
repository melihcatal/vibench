import asyncio
import threading
import queue as sync_queue
import pyaudio
from typing import AsyncGenerator, Any
from deepgram import DeepgramClient
from deepgram.types import LiveOptions, LiveTranscriptionEvents
from speech_client import DEEPGRAM_API_KEY
from speech_models import TranscriptChunk


async def stream_microphone() -> AsyncGenerator[TranscriptChunk, None]:
    client = DeepgramClient(DEEPGRAM_API_KEY)
    options = LiveOptions(
        model="nova-2-general",
        language="en-US",
        punctuate=True,
        interim_results=True,
        smart_format=True,
    )
    live = client.listen.live.v("1", options)
    transcript_queue: asyncio.Queue[TranscriptChunk] = asyncio.Queue()
    audio_queue: asyncio.Queue[bytes] = asyncio.Queue()
    closed = False

    def on_transcript(result: Any, **kwargs):
        if result.channel and result.channel.alternatives:
            text = result.channel.alternatives[0].transcript or ""
        else:
            text = ""
        is_final = result.is_final
        transcript_queue.put_nowait(TranscriptChunk(text=text, is_final=is_final))

    def on_close(result: Any, **kwargs):
        nonlocal closed
        closed = True

    live.registerHandler(LiveTranscriptionEvents.Transcript, on_transcript)
    live.registerHandler(LiveTranscriptionEvents.Close, on_close)
    await live.hold()

    async def send_loop():
        nonlocal closed
        while not closed:
            try:
                chunk = await asyncio.wait_for(audio_queue.get(), timeout=0.5)
                live.send(chunk)
            except asyncio.TimeoutError:
                continue
            except:
                break

    send_task = asyncio.create_task(send_loop())

    # Microphone setup
    CHUNK = 320
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()
    sync_audio_queue = sync_queue.Queue()

    def pyaudio_callback(in_data, frame_count, time_info, status):
        sync_audio_queue.put(in_data)
        return None, pyaudio.paContinue

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=pyaudio_callback,
    )
    stream.start_stream()

    loop = asyncio.get_running_loop()

    def audio_feeder():
        while stream.is_active() and not closed:
            try:
                chunk = sync_audio_queue.get(timeout=0.1)
                fut = asyncio.run_coroutine_threadsafe(audio_queue.put(chunk), loop)
                fut.result(timeout=1.0)
            except:
                pass

    feeder_thread = threading.Thread(target=audio_feeder, daemon=True)
    feeder_thread.start()

    try:
        while not closed:
            try:
                chunk = await asyncio.wait_for(transcript_queue.get(), timeout=1.0)
                yield chunk
            except asyncio.TimeoutError:
                continue
    finally:
        closed = True
        stream.stop_stream()
        stream.close()
        p.terminate()
        send_task.cancel()
        try:
            await live.finish()
        except:
            pass
