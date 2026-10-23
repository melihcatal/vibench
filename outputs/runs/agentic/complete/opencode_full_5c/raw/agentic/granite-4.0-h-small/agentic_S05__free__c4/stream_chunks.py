# [SAME-SCENARIO] stream_chunks.py
"""Stream audio chunks from an asynchronous source (e.g., a socket or file) and forward them to a streaming recognizer."""

import asyncio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client


async def stream_chunks(async_source, chunk_size=3200):
    """Yield audio chunks from an async iterable source."""
    client = get_speech_client()
    config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        ),
        interim_results=False,
    )
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in async_source
    )
    responses = client.streaming_recognize(config=config, requests=requests)
    async for response in responses:
        for result in response.results:
            if result.is_final:
                yield result.alternatives[0].transcript
            else:
                yield "\033[2K\rPartial: " + result.alternatives[0].transcript


# Example async source: a file opened in binary mode
# async def file_source(path):
#     with open(path, "rb") as f:
#         while True:
#             chunk = f.read(chunk_size)
#             if not chunk:
#                 break
#             yield chunk

if __name__ == "__main__":
    # placeholder - replace with actual async source
    pass
