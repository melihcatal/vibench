import asyncio
from google.cloud import speech


async def stream_with_language_and_punctuation(
    audio_chunks_async_generator,
    language_code="en-US",
    enable_automatic_punctuation=True,
    sample_rate_hertz=16000,
):
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    async def request_generator():
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(streaming_config, request_generator())

    async for response in responses:
        yield response
