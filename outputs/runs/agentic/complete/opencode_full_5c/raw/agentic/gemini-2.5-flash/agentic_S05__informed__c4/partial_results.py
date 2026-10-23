import asyncio
import os

from google.cloud import speech

# GOOGLE_APPLICATION_CREDENTIALS environment variable should be set


async def handle_partial_results(audio_source_async_generator):
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
        if result.is_final:
            print(f"Final transcript: {result.alternatives[0].transcript}")
            yield {"type": "final", "transcript": result.alternatives[0].transcript}
        else:
            print(f"Partial transcript: {result.alternatives[0].transcript}")
            yield {"type": "partial", "transcript": result.alternatives[0].transcript}
