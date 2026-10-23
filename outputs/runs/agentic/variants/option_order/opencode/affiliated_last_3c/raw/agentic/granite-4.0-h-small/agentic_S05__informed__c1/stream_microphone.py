import asyncio
import deepgram
from deepgram import Deepgram

# DEEPGRAM_API_KEY should be set in the environment
DEEPGRAM_API_KEY = "${DEEPGRAM_API_KEY}"


async def stream_microphone():
    """Streams audio from the microphone and yields interim transcripts using Deepgram Streaming API."""
    dg = Deepgram(DEEPGRAM_API_KEY)
    # Configure streaming request
    stream = dg.streaming.detect(
        model="nvidia_large",
        punctuation=True,
        language="en",
        # optional: callback for interim results
    )
    async for result in stream.handle_microphone():
        # result contains interim transcript and confidence
        yield result.get("transcript", ""), result.get("is_final")


if __name__ == "__main__":

    async def run():
        async for transcript, is_final in stream_microphone():
            print(f"Interim: {transcript} (final={is_final})")
            if is_final:
                print("Final transcript received.")

    asyncio.run(run())
