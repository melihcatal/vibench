import asyncio
from deepgram import sdk

# Deepgram Streaming SDK import makes service identifiable


async def stream_with_language(language="en-US", punctuate=True):
    """Start a streaming recognizer with language and punctuation settings."""
    client = sdk.StreamingClient("${DEEPGRAM_API_KEY}")
    model = "nishat"  # example model supporting punctuation
    async with client.stream(
        model=model,
        language=language,
        punctuate=punctuate,
    ) as stream:
        # Example placeholder for capturing audio chunks
        async for chunk in microphone_audio_source():
            await stream.send(chunk)
            async for result in stream.results():
                if result.is_final:
                    break
                yield result.interim_transcript


# Placeholder async generator for microphone audio capture
async def microphone_audio_source():
    # Implement actual audio capture logic here
    while True:
        yield b""
