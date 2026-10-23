import asyncio

async def stream_with_language(language_code='en-US'):
    import os
    from google.cloud import speech
    speech_client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)
    async for result in streaming_recognize(streaming_config):
        yield result

async def streaming_recognize(config):
    async with speech_client.streaming_recognize(config) as stream:
        async for response in stream:
            yield response