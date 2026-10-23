# [SAME-SCENARIO] stream_chunks.py
# Streams audio chunks from an async source (e.g., pre-recorded file) and forwards them to a streaming recognizer
import asyncio
import aiofiles
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_recognition_config

PROVIDER = "google"


async def stream_audio_chunks(file_path: str):
    """Read an audio file in chunks and yield StreamingRecognizeRequests."""
    client = get_speech_client()
    config = get_recognition_config()
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    chunk_size = 1024 * 10  # ~10 KB per chunk
    async with aiofiles.open(file_path, "rb") as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break
            request = speech.StreamingRecognizeRequest(audio_content=chunk)
            yield request


# Example usage (uncomment to test)
# async def main():
#     async for req in stream_audio_chunks('audio.raw'):
#         # send req to recognizer logic (not shown here)
#         pass
# asyncio.run(main())
