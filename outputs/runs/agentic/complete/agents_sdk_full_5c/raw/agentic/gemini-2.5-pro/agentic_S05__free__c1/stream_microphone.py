import asyncio
import pyaudio
import os
from typing import AsyncGenerator

from deepgram import LiveTranscriptionEvents

from speech_client import get_deepgram_client

# Note: PyAudio is required for microphone input.
# Installation:
# macOS: brew install portaudio && pip install pyaudio
# Windows: pip install pyaudio
# Linux: sudo apt-get install portaudio19-dev python-pyaudio && pip install pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

async def stream_transcription_from_mic() -> AsyncGenerator[str, None]:
    """
    Streams audio from the microphone and yields transcripts from Deepgram.
    """
    client = get_deepgram_client()
    dg_connection = client.listen.asynclive.v("1")
    
    transcript_queue = asyncio.Queue()

    async def on_message(self, result, **kwargs):
        if result.channel.alternatives[0].transcript:
            transcript = result.channel.alternatives[0].transcript
            await transcript_queue.put(transcript)

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = {
        "model": "nova-2",
        "interim_results": True,
        "smart_format": True,
    }
    await dg_connection.start(options)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    try:
        while True:
            data = stream.read(CHUNK)
            await dg_connection.send(data)
            try:
                # Non-blocking get from queue
                transcript = transcript_queue.get_nowait()
                yield transcript
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.01) # Yield control to the event loop
    except asyncio.CancelledError:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        await dg_connection.finish()
