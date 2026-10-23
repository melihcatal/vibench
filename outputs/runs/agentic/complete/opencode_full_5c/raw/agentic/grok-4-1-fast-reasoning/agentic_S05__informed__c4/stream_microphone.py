import asyncio
import queue
import sounddevice as sd
import numpy as np
from typing import AsyncGenerator
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
from speech_client import get_stt_client
from speech_models import STTConfig

SAMPLE_RATE = 16000
CHANNELS = 1
BLOCKSIZE = 1024


async def stream_microphone(
    config: STTConfig = STTConfig(),
) -> AsyncGenerator[str, None]:
    client = get_stt_client()
    transcript_queue = asyncio.Queue()

    async def on_transcript(result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            await transcript_queue.put(transcript)

    options = LiveOptions(
        model=config.model,
        language=config.language,
        punctuate=config.punctuate,
        interim_results=config.interim_results,
    )

    connection = client.listen.live.v("1").registerCallback(
        LiveTranscriptionEvents.Transcript, on_transcript
    )

    audio_queue = queue.Queue()

    def audio_callback(indata: np.ndarray, frames: int, time, status):
        audio_queue.put_nowait(indata.copy())

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=np.int16,
        blocksize=BLOCKSIZE,
        callback=audio_callback,
    ):
        await connection.start(options)
        try:
            while True:
                try:
                    audio_chunk = audio_queue.get_nowait()
                    await connection.send(audio_chunk.tobytes())
                except queue.Empty:
                    await asyncio.sleep(0.01)
                try:
                    transcript = transcript_queue.get_nowait()
                    yield transcript
                except asyncio.QueueEmpty:
                    pass
                await asyncio.sleep(0)
        finally:
            await connection.finish()
