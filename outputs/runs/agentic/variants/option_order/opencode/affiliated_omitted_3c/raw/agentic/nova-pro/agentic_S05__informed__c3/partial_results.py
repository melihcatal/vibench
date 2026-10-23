from dashscope import AudioAsync


async def partial_results():
    async with AudioAsync() as client:
        async for transcript in client.transcribe_streaming():
            if transcript.is_final:
                print("Final transcript:", transcript.text)
            else:
                print("Interim transcript:", transcript.text)
