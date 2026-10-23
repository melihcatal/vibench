import asyncio
import numpy as np
import sounddevice as sd
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents
from speech_client import get_stt_client
from speech_models import StreamingConfig, create_live_options

async def stream_microphone(config: StreamingConfig = StreamingConfig()) -> AsyncGenerator[tuple[str, str], None]:
    client = get_stt_client()
    connection = client.listen.live.v(config.version)
    options = create_live_options(config)
    transcript_queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def on_transcript(result, **_):
        alt = result.channel.alternatives[0]
        text = alt.transcript or ""
        typ = "final" if result.speech_final else "interim"
        asyncio.run_coroutine_threadsafe(transcript_queue.put((typ, text)), loop)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    await connection.start(options)

    samplerate = 16000
    channels = 1
    blocksize = 1280

    def audio_callback(indata: np.ndarray, frames: int, time_info, status):
        audio = (indata[:, 0] * 32767).astype(np.int16)
        audio_bytes = audio.tobytes()
        connection.send(audio_bytes)

    try:
        with sd.InputStream(samplerate=samplerate, channels=channels, dtype='float32',
                            blocksize=blocksize, callback=audio_callback):
            while True:
                typ, text = await asyncio.wait_for(transcript_queue.get(), timeout=1.0)
                yield typ, text
    except asyncio.CancelledError:
        pass
    finally:
        await connection.finish()
