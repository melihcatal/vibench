import asyncio
from google.cloud import speech


async def stream_audio_chunks(
    audio_chunks_async_generator, sample_rate_hertz=16000, language_code="en-US"
):
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16, adjust if needed
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
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
