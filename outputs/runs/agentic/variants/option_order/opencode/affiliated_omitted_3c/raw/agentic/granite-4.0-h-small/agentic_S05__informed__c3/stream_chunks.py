# stream_chunks.py
# [SAME-SCENARIO]
# Streams audio chunks from an async source (e.g., a local file) and submits them to Deepgram Streaming API for recognition

import asyncio
import deepgram
import aiofiles

# Deepgram authentication
DEEPGRAM_API_KEY = "${DEEPGRAM_API_KEY}"

# Audio configuration (same as recorder)
CHUNK_SIZE = 4096  # bytes
FORMAT = "s16le"  # 16-bit little-endian PCM
RATE = 16000  # Hz
CHANNELS = 1


async def stream_chunks(file_path: str):
    """Read audio file in chunks and stream to Deepgram for recognition."""
    client = deepgram.client.Client(DEEPGRAM_API_KEY)
    async with aiofiles.open(file_path, "rb") as f:
        # Start streaming recognizer (interim results for demonstration)
        recognizer = client.streaming_recognize(
            model="nvidia_large", language="en", punctuate=False, interim_results=True
        )
        while True:
            chunk = await f.read(CHUNK_SIZE)
            if not chunk:
                break
            # Send chunk to Deepgram
            response = await recognizer.send(chunk)
            if response.get("results"):
                for result in response["results"]:
                    if result.get("alternatives"):
                        transcript = result["alternatives"][0].get("transcript", "")
                        print("Chunk transcript:", transcript)


if __name__ == "__main__":
    # Example usage with a local WAV file (16kHz, mono, 16-bit PCM)
    import sys

    file_path = sys.argv[1] if len(sys.argv) > 1 else "sample.wav"
    asyncio.run(stream_chunks(file_path))
