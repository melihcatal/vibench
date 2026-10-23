import asyncio
import json
from deepgram import Deepgram


# Define a helper async generator to stream microphone audio (placeholder implementation)
async def microphone_generator():
    # Placeholder: simulate yielding audio chunks
    for i in range(5):
        yield b"dummy audio chunk"
        await asyncio.sleep(0.5)


async def main():
    # Deepgram credentials (replace with your own)
    DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"
    client = Deepgram(DeepgramCredentials(api_key=DEEPGRAM_API_KEY))

    source = client.listen(
        # The listen method accepts an async iterable of bytes
        source=microphone_generator()
    )
    async for result in source.listen():
        # Deepgram returns interim and final results; handle accordingly
        if result.get("is_final"):
            print(json.dumps(result))


if __name__ == "__main__":
    asyncio.run(main())
