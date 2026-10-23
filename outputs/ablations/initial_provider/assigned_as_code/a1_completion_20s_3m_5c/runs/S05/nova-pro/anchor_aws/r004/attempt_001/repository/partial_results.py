from google.cloud import speech
from speech_client import create_speech_client
from speech_models import create_streaming_config

async def partial_results(stream):
    client = create_speech_client()
    config = create_streaming_config('en-US', True)
    async for request in stream:
        response = client.streaming_recognize(config, [request])
        for result in response.results:
            if not result.is_final:
                yield result.alternatives[0].transcript
            else:
                yield result.alternatives[0].transcript