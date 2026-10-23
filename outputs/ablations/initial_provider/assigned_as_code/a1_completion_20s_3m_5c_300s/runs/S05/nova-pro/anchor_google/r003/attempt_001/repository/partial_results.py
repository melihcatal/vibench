from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
from speech_models import create_streaming_config

async def handle_partial_results(stream):
    async for response in stream:
        for result in response.results:
            if not result.is_final:
                print(f"Interim transcript: {result.alternatives[0].transcript}")
            else:
                print(f"Final transcript: {result.alternatives[0].transcript}")