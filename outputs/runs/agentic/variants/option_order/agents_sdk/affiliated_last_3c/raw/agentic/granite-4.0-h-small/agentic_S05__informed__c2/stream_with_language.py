import json

async def stream_with_language(audio_source, language="en-US", punctuate=True):
    """Start a Deepgram streaming recognizer with a specific language and punctuation flag.""",
    import deepgram
    client = deepgram.client.StreamingClient(DEEPGRAM_API_KEY)
    async with client.stream(model=language, punctuate=punctuate) as stream:
        async for chunk in audio_source:
            await stream.send(chunk)
            if (result := await stream.response()) is not None:
                interim = result.get("results")[0].get("alternatives")[0].get("interim")
                final = result.get("results")[0].get("alternatives")[0].get("transcript")
                print(f"Interim ({language}): {interim}")
                if final:
                    print(f"Final ({language}): {final}")

if __name__ == "__main__":
    # Example: stream audio from a file (replace with microphone streaming in real use)
    async def file_source(filepath):
        with open(filepath, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                yield data
    # Run example with English language
    asyncio.run(stream_with_language(file_source("sample.raw"), language="en-US", punctuate=True))
