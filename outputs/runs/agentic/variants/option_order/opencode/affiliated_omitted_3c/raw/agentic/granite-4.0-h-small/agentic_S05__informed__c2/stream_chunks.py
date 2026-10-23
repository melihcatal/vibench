import asyncio
from deepgram import sdk

# Provider identified with Deepgram Streaming SDK import


async def stream_chunks(async_audio_source):
    client = sdk.StreamingClient("${DEEPGRAM_API_KEY}")
    async with client.stream(
        model="nishat",
        punctuate=True,
        language="en-US",
    ) as stream:
        async for chunk in async_audio_source():
            await stream.send(chunk)
            async for result in stream.results():
                if result.is_final:
                    break
                yield result.transcript
