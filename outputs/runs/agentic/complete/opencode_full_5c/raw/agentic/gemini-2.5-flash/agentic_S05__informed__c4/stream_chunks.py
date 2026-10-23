import asyncio
import os

from google.cloud import speech

# GOOGLE_APPLICATION_CREDENTIALS environment variable should be set


async def stream_audio_chunks(audio_source_async_generator):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def request_generator():
        async for chunk in audio_source_async_generator():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests = request_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield transcript
