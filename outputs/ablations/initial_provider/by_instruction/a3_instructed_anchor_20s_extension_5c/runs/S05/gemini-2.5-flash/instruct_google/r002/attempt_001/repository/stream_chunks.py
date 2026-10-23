import asyncio
from google.cloud import speech_v1p1beta1 as speech


async def stream_audio_chunks(audio_source_async_iter):
    language_code = "en-US"

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        model="video",
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    async def request_generator():
        async for chunk in audio_source_async_iter:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests = request_generator()
    responses = await client.streaming_recognize(streaming_config, requests)

    async for response in responses:
        yield response
