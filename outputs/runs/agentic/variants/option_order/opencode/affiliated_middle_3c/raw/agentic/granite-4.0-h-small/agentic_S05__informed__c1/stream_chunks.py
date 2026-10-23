import asyncio
import json
from deepgram import Deepgram


# Helper to simulate an async source yielding raw audio bytes
async def async_audio_source():
    # Example: fetch audio chunks from a network source (placeholder)
    for i in range(5):
        yield b"audio_chunk_sample_"
        await asyncio.sleep(0.4)


async def main():
    DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"
    client = Deepgram(DeepgramCredentials(api_key=DEEPGRAM_API_KEY))

    source = client.listen(
        # Listen expects an async iterable of bytes; we use our async source
        source=async_audio_source()
    )
    async for result in source.listen():
        # Emit partial/transcript chunks as they arrive
        partial = result.get("partial")
        if partial:
            print(json.dumps({"partial": partial}))


if __name__ == "__main__":
    asyncio.run(main())
