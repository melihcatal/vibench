import asyncio
import pyaudio
import threading
from typing import AsyncIterator
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from speech_client import client
from speech_models import (
    TranscriptChunk,
    LiveOptions,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    AUDIO_FRAME_SIZE,
)


async def stream_microphone(
    options: LiveOptions = None,
) -> AsyncIterator[TranscriptChunk]:
    if options is None:
        options = {}
    p = pyaudio.PyAudio()
    audio_stream = p.open(
        format=pyaudio.paInt16,
        channels=AUDIO_CHANNELS,
        rate=AUDIO_SAMPLE_RATE,
        input=True,
        frames_per_buffer=AUDIO_FRAME_SIZE,
        input_device_index=None,
    )

    transcript_queue = asyncio.Queue()

    def on_message(message):
        if message.type == "Transcript":
            alt = message.channel.alternatives[0]
            chunk: TranscriptChunk = {
                "transcript": alt.transcript,
                "is_final": message.is_final,
                "confidence": alt.confidence,
            }
            asyncio.get_running_loop().call_soon_threadsafe(
                lambda: asyncio.create_task(transcript_queue.put(chunk))
            )

    connection = client.listen.v2.connect(
        model=options.get("model", "nova-2"),
        sample_rate=AUDIO_SAMPLE_RATE,
        channels=AUDIO_CHANNELS,
        encoding="linear16",
        language=options.get("language", "en"),
        punctuate=options.get("punctuate", True),
        interim_results=options.get("interim_results", True),
    )

    connection.on(EventType.MESSAGE, on_message)

    def send_audio():
        try:
            while True:
                data = audio_stream.read(AUDIO_FRAME_SIZE, exception_on_overflow=False)
                connection.send(data)
        except:
            pass

    sender_thread = threading.Thread(target=send_audio, daemon=True)
    sender_thread.start()

    connection.start_listening()

    try:
        while True:
            chunk = await transcript_queue.get()
            yield chunk
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
        connection.finish()
