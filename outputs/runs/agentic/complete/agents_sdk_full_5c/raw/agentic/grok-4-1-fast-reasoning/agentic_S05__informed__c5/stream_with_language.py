import asyncio
import queue
import threading
import pyaudio
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents
from speech_client import get_speech_client
from speech_models import get_live_options

async def stream_microphone_with_language(language: str = 'es', punctuate: bool = True) -> AsyncGenerator[str, None]:
    client = get_speech_client()
    options = get_live_options(language=language, punctuate=punctuate)
    transcript_queue = asyncio.Queue()
    p = pyaudio.PyAudio()
    RATE = 16000
    CHUNK = int(RATE * 0.1)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    audio_queue = queue.Queue()

    def audio_callback(in_data, frame_count, time_info, status):
        audio_queue.put(in_data)
        return (None, pyaudio.paContinue)

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=audio_callback,
    )
    stream.start_stream()

    connection = client.listen.live.v("1", options)

    def on_transcript(result):
        try:
            transcript = result.channel.alternatives[0].transcript
            if transcript.strip():
                loop = asyncio.get_event_loop()
                loop.call_soon_threadsafe(transcript_queue.put_nowait, transcript)
        except Exception:
            pass

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    def send_audio():
        while True:
            try:
                chunk = audio_queue.get(timeout=1)
                connection.send(chunk)
            except queue.Empty:
                pass
            except Exception:
                break

    sender_thread = threading.Thread(target=send_audio, daemon=True)
    sender_thread.start()
    connection.start()

    try:
        while True:
            yield await transcript_queue.get()
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        connection.finish()
