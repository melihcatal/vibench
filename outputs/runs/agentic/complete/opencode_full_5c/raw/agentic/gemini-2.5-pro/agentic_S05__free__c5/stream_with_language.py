import asyncio
from google.cloud import speech
from speech_client import get_speech_client


async def stream_with_language_settings(
    audio_chunk_generator, language_code="es-ES", enable_punctuation=False
):
    client = get_speech_client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    async def request_generator():
        async for chunk in audio_chunk_generator():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(streaming_config, request_generator())

    async for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
