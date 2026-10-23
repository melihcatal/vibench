import asyncio

async def partial_results():
    async for result in streaming_recognize():
        if result.results:
            for res in result.results:
                if res.is_final:
                    yield 'Final: ' + res.alternatives[0].transcript
                else:
                    yield 'Interim: ' + res.alternatives[0].transcript

async def streaming_recognize(config):
    import os
    from google.cloud import speech
    speech_client = speech.SpeechClient()
    async with speech_client.streaming_recognize(config) as stream:
        async for response in stream:
            yield response