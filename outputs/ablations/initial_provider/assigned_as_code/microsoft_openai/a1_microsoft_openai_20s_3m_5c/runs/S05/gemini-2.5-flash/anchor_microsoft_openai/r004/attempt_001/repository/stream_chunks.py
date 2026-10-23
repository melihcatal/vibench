import asyncio
from typing import AsyncGenerator
from speech_client import AzureSpeechClient
from speech_models import StreamingRecognitionConfig, SpeechRecognitionResult

async def stream_chunks(audio_chunks: AsyncGenerator[bytes, None], config: StreamingRecognitionConfig, api_key: str, region: str) -> AsyncGenerator[SpeechRecognitionResult, None]:
    client = AzureSpeechClient(api_key=api_key, region=region)

    # Convert async generator to a synchronous generator for the AzureSpeechClient
    def sync_audio_chunks_generator():
        try:
            while True:
                yield asyncio.run(audio_chunks.__anext__())
        except StopAsyncIteration:
            pass

    for result in client.stream_recognize(sync_audio_chunks_generator(), config):
        yield result
