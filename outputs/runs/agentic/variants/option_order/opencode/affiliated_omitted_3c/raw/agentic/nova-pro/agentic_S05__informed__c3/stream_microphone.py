from dashscope import AudioAsync


async def stream_microphone():
    async with AudioAsync() as client:
        async for transcript in client.transcribe_streaming():
            yield transcript
