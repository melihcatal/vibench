import os
from google.cloud import speech


async def stream_audio_chunks(audio_chunks_async_source):
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
        async for chunk in audio_chunks_async_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(streaming_config, request_generator())

    async for response in responses:
        for result in response.results:
            yield result.alternatives[0].transcript
