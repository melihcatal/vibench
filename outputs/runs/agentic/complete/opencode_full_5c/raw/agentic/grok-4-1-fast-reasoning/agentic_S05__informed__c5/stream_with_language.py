import asyncio
import pyaudio
import threading
from typing import AsyncIterator
from speech_client import client
from speech_models import (
    TranscriptChunk,
    LiveOptions,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    AUDIO_FRAME_SIZE,
)
from deepgram.core.events import EventType
from deepgram import DeepgramClient


async def stream_with_language(
    language: str = "fr", options: LiveOptions = None
) -> AsyncIterator[TranscriptChunk]:
    if options is None:
        options = {}
    options["language"] = language
    options["punctuate"] = True
    # same as stream_microphone
    p = pyaudio.PyAudio()
    audio_stream = p.open(
        format=pyaudio.paInt16,
        channels=AUDIO_CHANNELS,
        rate=AUDIO_SAMPLE_RATE,
        input=True,
        frames_per_buffer=AUDIO_FRAME_SIZE,
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

    connection = client.listen.v2.connect(**options)

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
