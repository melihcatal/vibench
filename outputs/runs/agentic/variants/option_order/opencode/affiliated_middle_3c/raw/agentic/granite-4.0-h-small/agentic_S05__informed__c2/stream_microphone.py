import asyncio
import deepgram

# Deepgram Streaming API integration
# Define configuration and API key
DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"


async def stream_microphone():
    """Streams microphone audio using Deepgram's Streaming API and yields interim transcripts."""
    client = deepgram.StreamingClient(DEEPGRAM_API_KEY)
    # Start a streaming session
    async with client.start_language("en-US") as stream:
        # This part would normally capture audio from a microphone
        # For demonstration, we simulate audio chunks with async sleep
        async for interim in stream.listen():
            if interim["is_final"]:
                yield interim["alternatives"][0]["transcript"]
            else:
                yield interim["alternatives"][0]["transcript"]


# Example usage (not executed here)
# asyncio.run(async for transcript in stream_microphone()):
#     print(transcript)
