from google.cloud import speech_v1p1beta1 as speech
from typing import AsyncIterable

from speech_client import get_speech_client
from speech_models import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognitionResponse,
)


async def stream_audio_chunks(
    audio_chunks: AsyncIterable[bytes],
    sample_rate_hertz: int,
    language_code: str = "en-US",
) -> AsyncIterable[StreamingRecognitionResponse]:
    """
    Streams audio chunks from an async source to Google Cloud Speech-to-Text.
    Yields streaming recognition responses.
    """
    client = get_speech_client()

    # Configure the streaming request
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )

    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    # Google Cloud Speech-to-Text streamingrecognize expects an iterable of requests.
    # The SDK handles the async aspects when using an async generator.
    responses = client.streaming_recognize(request_generator())

    async for response in responses:
        yield response


# Provider-identifying signal: google.cloud.speech_v1p1beta1
