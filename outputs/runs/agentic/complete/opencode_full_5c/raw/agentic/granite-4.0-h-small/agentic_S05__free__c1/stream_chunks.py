import asyncio
import json

from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_google_client

CHUNK_SIZE = 320  # 20 ms for 16kHz 16-bit audio
LANGUAGE_CODE = "en-US"
ENCODING = speech.RecognitionConfig.AudioEncoding.LINEAR16


async def read_audio_chunks(source_async_generator):
    """Read binary audio chunks from any async generator."""
    while True:
        chunk = await source_async_generator.__anext__()
        if not chunk:
            break
        yield chunk


def chunk_to_recognition_chunk(chunk: bytes):
    return {
        "audio_content": chunk,
    }


async def main(source_async_iterable):
    client = get_google_client()
    config = speech.RecognitionConfig(
        encoding=ENCODING,
        sample_rate_hertz=16000,
        language_code=LANGUAGE_CODE,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = []
    async for chunk in read_audio_chunks(source_async_iterable):
        requests.append(speech.StreamingRecognizeRequest(audio=chunk))
        if len(requests) >= 5:  # batch at most 5 chunks (~100ms)
            await client.streaming_recognize(streaming_config, requests)
            requests = []
    if requests:
        await client.streaming_recognize(streaming_config, requests)


if __name__ == "__main__":
    # Example usage with a simulated async byte stream
    async def dummy_chunks():
        for i in range(20):
            yield b"a" * CHUNK_SIZE

    asyncio.run(main(dummy_chunks()))
