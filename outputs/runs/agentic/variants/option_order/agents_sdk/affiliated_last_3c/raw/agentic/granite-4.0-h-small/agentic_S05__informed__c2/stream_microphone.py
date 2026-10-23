import asyncio
import json
import sys
from typing import AsyncIterable

import deepgram

# Deepgram Streaming API client configuration
DEEPGRAM_API_KEY = "${DEEPGRAM_API_KEY}"

async def microphone_stream(sample_rate: int = 16000, chunk_size: int = 4096) -> AsyncIterable[bytes]:
    """Yield raw PCM audio from the default microphone.
    Args:
        sample_rate: Sampling rate of the audio.
        chunk_size: Number of bytes per chunk.
    """
    try:
        import sounddevice as sd
    except ImportError:
        print("sounddevice library not installed; please run `pip install sounddevice`", file=sys.stderr)
        raise
    stream = sd.InputStream(sample_rate=sample_rate, channels=1, dtype='int16',
                             callback=lambda data, frames, time, status: data.tobytes() if not status else None)
    async def _gen():
        with stream:
            while True:
                data = stream.read(chunk_size)
                if data is None:
                    break
                yield data
    return _gen()

async def stream_recognizer(audio_stream: AsyncIterable[bytes], model: str = "english", punctuate: bool = True) -> None:
    """Stream audio to Deepgram real‑time speech‑to‑text and print interim results.
    Args:
        audio_stream: An async iterable yielding raw audio bytes.
        model: Language/model identifier supported by Deepgram.
        punctuate: Whether to add punctuation.
    """
    client = deepgram.client.StreamingClient(DEEPGRAM_API_KEY)
    async with client.stream(model=model, punctuate=punctuate) as stream:
        async for chunk in audio_stream:
            await stream.send(chunk)
            if (result := await stream.response()) is not None:
                interim = result.get("results")[0].get("alternatives")[0].get("interim")
                final = result.get("results")[0].get("alternatives")[0].get("transcript")
                print("Interim:", interim)
                if final:
                    print("Final :", final)

if __name__ == "__main__":
    asyncio.run(stream_recognizer(microphone_stream()))