from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
from speech_models import create_streaming_config

async def stream_with_language(language_code, enable_automatic_punctuation):
    client = get_speech_client()
    streaming_config = create_streaming_config(language_code, enable_automatic_punctuation)
    async with client.streaming_recognize(streaming_config) as stream:
        async for response in stream:
            for result in response.results:
                if not result.is_final:
                    print(f"Interim transcript: {result.alternatives[0].transcript}")
                else:
                    print(f"Final transcript: {result.alternatives[0].transcript}")