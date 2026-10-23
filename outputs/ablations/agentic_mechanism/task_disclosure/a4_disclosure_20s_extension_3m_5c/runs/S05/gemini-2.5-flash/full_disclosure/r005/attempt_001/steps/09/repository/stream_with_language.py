import asyncio

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types


async def stream_with_language(
    audio_chunks,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    """Starts a streaming recognizer with language and punctuation settings."""

    client = speech.SpeechClient()

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

    async def request_generator():
        yield types.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunks:
            yield types.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(request_generator())

    async for response in responses:
        yield response
