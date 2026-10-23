import asyncio
from deepgram import sdk

# Deepgram Streaming SDK import makes provider identifiable


async def stream_microphone():
    # Set up Deepgram client using environment variable for API key
    client = sdk.StreamingClient("${DEEPGRAM_API_KEY}")
    # Configure streaming recognizer with microphone audio source
    async with client.stream(
        model="nishat",  # example model
        punctuate=True,
        language="en-US",
    ) as stream:
        # Start microphone capture (placeholder for actual audio capture)
        async for chunk in microphone_audio_source():
            await stream.send(chunk)
            # Yield interim transcripts as they become available
            async for result in stream.results():
                if result.is_final:
                    break
                yield result.interim_transcript


# Placeholder async generator for microphone audio capture
async def microphone_audio_source():
    # Implement actual audio capture logic here
    while True:
        yield b""
