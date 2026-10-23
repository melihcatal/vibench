import asyncio
import json
from deepgram import Deepgram


async def main():
    # Deepgram credentials (replace with real key)
    DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"
    client = Deepgram(DeepgramCredentials(api_key=DEEPGRAM_API_KEY))

    # Simulate an async audio stream (placeholder)
    async def audio_chunks():
        for i in range(3):
            yield b"sample_audio_"
            await asyncio.sleep(0.3)

    # Build a config with language and punctuation options
    listen_config = {"language": "en-US", "punctuation": True, "format": "json"}

    # Bind the audio iterable to Deepgram listening
    source = client.listen(source=audio_chunks(), **listen_config)
    async for result in source.listen():
        # Print each (partial or final) result with metadata
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
