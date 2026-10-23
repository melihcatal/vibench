import asyncio
import os

from google.cloud import speech_v1p1beta1 as speech


async def stream_chunks_from_async_source(
    audio_chunks_source, language_code: str = "en-US"
):
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Assuming 16kHz for general audio chunks
        language_code=language_code,
        model="default",
        use_enhanced=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def request_generator():
        async for chunk in audio_chunks_source:
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
        yield transcript, result.is_final
