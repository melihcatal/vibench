import asyncio
import aiohttp
import json
from dotenv import load_dotenv
import speech_client as sc

load_dotenv()

def chunks(data, size=1024):
    for i in range(0, len(data), size):
        yield data[i:i+size]

async def stream_chunks(audio_source):
    # Assume audio_source is an async iterable producing bytes
    async for chunk in audio_source:
        # Forward each byte stream chunk to the streaming recognizer
        response = await sc.send_streaming_request(chunk)
        yield sc.parse_partial_results(response)

if __name__ == "__main__":
    # Example usage with a file audio source
    import aiofiles
    async with aiofiles.open('sample.flac', mode='rb') as f:
        async for audio_chunk in f:
            async for result in stream_chunks(audio_chunk):
                print(result)
