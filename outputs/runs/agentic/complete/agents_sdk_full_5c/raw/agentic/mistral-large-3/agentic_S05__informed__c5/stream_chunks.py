import asyncio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamingConfig

async def stream_audio_chunks(audio_source):
    client = get_speech_client()
    config = StreamingConfig().get_recognition_config()
    streaming_config = types.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def request_stream():
        async for chunk in audio_source:
            yield types.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(streaming_config, request_stream())
    async for response in responses:
        for result in response.results:
            yield result