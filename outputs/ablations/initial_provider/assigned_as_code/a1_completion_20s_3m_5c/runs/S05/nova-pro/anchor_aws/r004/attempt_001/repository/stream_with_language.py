from google.cloud import speech
from speech_client import create_speech_client
from speech_models import create_streaming_config

async def stream_with_language(language_code, enable_automatic_punctuation):
    client = create_speech_client()
    config = create_streaming_config(language_code, enable_automatic_punctuation)
    async for request in stream_audio_chunks('https://example.com/audio'):
        response = client.streaming_recognize(config, [request])
        for result in response.results:
            if not result.is_final:
                yield result.alternatives[0].transcript
            else:
                yield result.alternatives[0].transcript