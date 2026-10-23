import asyncio
import sounddevice as sd
import numpy as np
from typing import AsyncGenerator
import sys
from speech_client import dg_client
from speech_models import TranscriptChunk
from deepgram import LiveOptions, LiveTranscriptionEvents
from deepgram.types.live import LiveTranscriptResult


async def stream_microphone() -> AsyncGenerator[TranscriptChunk, None]:
    sample_rate = 16000
    channels = 1
    blocksize = 3200  # ~200ms

    trans_queue: asyncio.Queue[TranscriptChunk] = asyncio.Queue()

    def transcript_handler(transcript: LiveTranscriptResult):
        if transcript.channel and transcript.channel.alternatives:
            text = transcript.channel.alternatives[0].transcript or ""
            is_final = transcript.is_final
            trans_queue.put_nowait(TranscriptChunk(text=text, is_final=is_final))

    connection = dg_client.listen.live.v("1")

    connection.on(LiveTranscriptionEvents.Transcript, transcript_handler)

    options = LiveOptions(
        model="nova-2",
        sample_rate=sample_rate,
        channels=channels,
        interim_results=True,
        language="en",
        punctuate=True,
    )

    def audio_callback(indata: np.ndarray, frames: int, time_info, status):
        if status:
            print(status, file=sys.stderr)
        connection.send(indata.tobytes())

    stream = sd.InputStream(
        samplerate=sample_rate,
        channels=channels,
        blocksize=blocksize,
        dtype="int16",
        callback=audio_callback,
    )

    with stream:
        await connection.start(options)
        try:
            while True:
                chunk = await trans_queue.get()
                yield chunk
        finally:
            await connection.finish()
