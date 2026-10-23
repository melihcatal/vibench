import asyncio
import os
from typing import AsyncIterator, Optional

from google.cloud import speech


def _audio_stream(record_seconds: float = 0.0) -> AsyncIterator[bytes]:
    try:
        import pyaudio
    except Exception as exc:
        raise RuntimeError("pyaudio is required for microphone streaming") from exc

    sample_rate = 16000
    chunk_size = int(sample_rate / 10)
    audio_format = pyaudio.paInt16
    channels = 1

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=audio_format,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    async def generator() -> AsyncIterator[bytes]:
        start = asyncio.get_event_loop().time()
        try:
            while True:
                if record_seconds > 0 and (asyncio.get_event_loop().time() - start) >= record_seconds:
                    break
                data = await asyncio.to_thread(stream.read, chunk_size, False)
                yield data
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()

    return generator()


async def stream_microphone(language_code: str = "en-US", punctuation: bool = True, record_seconds: float = 0.0) -> AsyncIterator[str]:
    client = speech.SpeechAsyncClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=punctuation,
        model="latest_long",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        single_utterance=False,
    )

    async def requests() -> AsyncIterator[speech.StreamingRecognizeRequest]:
        async for chunk in _audio_stream(record_seconds=record_seconds):
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(streaming_config=streaming_config, requests=requests())
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript


__all__ = ["stream_microphone"]
