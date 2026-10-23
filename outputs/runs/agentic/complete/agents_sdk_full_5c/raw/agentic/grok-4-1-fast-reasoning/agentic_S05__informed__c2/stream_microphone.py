import asyncio
import sounddevice as sd
import numpy as np
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
from typing import AsyncGenerator
from speech_client import get_speech_config
from speech_models import pcm16_to_bytes, AudioConfig

async def stream_microphone() -> AsyncGenerator[str, None]:
    config = get_speech_config('deepgram')
    api_key = config['api_key']
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY not set")

    deepgram = DeepgramClient(api_key)

    transcript_queue: asyncio.Queue[str] = asyncio.Queue()

    def on_transcript(event: dict):
        if 'channel' in event and event['channel']['alternatives']:
            transcript = event['channel']['alternatives'][0]['transcript']
            if transcript:
                asyncio.create_task(transcript_queue.put(transcript))

    connection = deepgram.listen.live.v("1")
    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    options = LiveOptions(
        model="nova-2-general",
        language="en",
        punctuate=True,
        interim_results=True,
        smart_format=True
    )

    await connection.start(options)

    sample_rate = AudioConfig().sample_rate_hertz
    blocksize = int(sample_rate * 0.03)

    def callback(indata: np.ndarray, frames: int, time_info, status):
        if status:
            pass
        audio_bytes = pcm16_to_bytes(indata[:, 0])
        asyncio.create_task(connection.send(audio_bytes))

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype=np.float32,
        blocksize=blocksize,
        callback=callback
    ):
        try:
            while True:
                transcript = await transcript_queue.get()
                yield transcript
        finally:
            await connection.finish()