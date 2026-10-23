import os
import asyncio
import pyaudio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from speech_client import get_deepgram_client
from speech_models import TranscriptEvent

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

async def stream_microphone():
    deepgram = get_deepgram_client()
    dg_connection = deepgram.listen.asynclive.v("1")

    async def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            event = TranscriptEvent(
                text=transcript,
                is_final=result.is_final,
                confidence=result.channel.alternatives[0].confidence
            )
            yield event

    dg_connection.on(LiveTranscriptionEvents.TranscriptReceived, on_message)

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        smart_format=True,
        interim_results=True,
        punctuate=True
    )

    await dg_connection.start(options)

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192
    )

    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            await dg_connection.send(data)
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        await dg_connection.finish()

async def microphone_transcript_stream():
    async for event in stream_microphone():
        yield event