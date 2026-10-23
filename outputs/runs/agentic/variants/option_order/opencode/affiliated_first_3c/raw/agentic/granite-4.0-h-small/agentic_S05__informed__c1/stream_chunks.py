import asyncio
import aiohttp
import os

# Use Deepgram Streaming API
# Credentials: DEEPGRAM_API_KEY


async def chunk_stream(source_generator):
    """
    source_generator: async generator yielding bytes of audio chunks
    """
    api_key = os.getenv("DEEPGRAM_API_KEY")
    url = "https://api.deepgram.com/v1/listen"

    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "audio/l16; rate=16000",
        }
        async with session.post(url, headers=headers, timeout=300) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Deepgram request failed: {resp.status}")
            async for chunk in source_generator:
                if not chunk:
                    break
                await resp.write(chunk)
                async for line in resp.content:
                    # Deepgram streams interim results
                    data = line.decode("utf-8").strip()
                    if data:
                        print("Interim:", data)
            # Final result
            final = await resp.json()
            print(
                "Final transcript:",
                final.get("results", [{}])[0]
                .get("alternatives", [{}])[0]
                .get("transcript", ""),
            )


if __name__ == "__main__":
    # Example async generator of audio chunks
    async def audio_source():
        for _ in range(5):
            await asyncio.sleep(0.5)
            yield b"audio_data..."  # Replace with real audio reads

    asyncio.run(chunk_stream(audio_source()))
