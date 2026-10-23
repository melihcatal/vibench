import asyncio


async def stream_microphone():
    """Streams microphone audio and yields interim transcripts using Deepgram Streaming API."""
    import deepgram

    client = deepgram.transcription.StreamingClient()
    # Set up audio source (e.g., using pyaudio or similar)
    # Placeholder for actual audio capture loop
    async for interim in client.transcribe(interim=True):
        yield interim


# Usage: asyncio.run(async for t in stream_microphone(): print(t))
