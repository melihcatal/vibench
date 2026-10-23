import os
import asyncio
import pyaudio
from deepgram import Deepgram
from speech_client import get_deepgram_client
from speech_models import TranscriptEvent

deepgram = get_deepgram_client()

async def stream_microphone():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192
    )

    try:
        dg_connection = await deepgram.transcription.live({
            "punctuate": True,
            "interim_results": True,
            "language": "en-US",
            "model": "nova-2"
        })

        async def send_audio():
            while True:
                data = stream.read(8192, exception_on_overflow=False)
                await dg_connection.send(data)
                await asyncio.sleep(0.1)

        async def receive_transcripts():
            async for event in dg_connection:
                transcript_event = TranscriptEvent.from_deepgram(event)
                if transcript_event:
                    yield transcript_event

        send_task = asyncio.create_task(send_audio())
        try:
            async for transcript in receive_transcripts():
                yield transcript
        finally:
            send_task.cancel()
            await dg_connection.finish()

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()