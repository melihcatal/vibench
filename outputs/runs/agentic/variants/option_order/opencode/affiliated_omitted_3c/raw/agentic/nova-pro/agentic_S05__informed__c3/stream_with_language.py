from dashscope import AudioAsync


async def stream_with_language():
    async with AudioAsync() as client:
        async for transcript in client.transcribe_streaming(
            language="en-US", punctuation=True
        ):
            yield transcript
