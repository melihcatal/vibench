from typing import AsyncIterable
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig, StreamingRecognitionResponse

async def stream_with_language_and_punctuation(
    audio_chunks: AsyncIterable[bytes],
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    rate: int = 16000
) -> StreamingRecognitionResponse:
    """Starts a streaming recognizer with language and punctuation settings."""

    client = get_speech_client()

    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=rate,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = StreamingRecognitionConfig(config=audio_config, interim_results=True)

    async def generate_requests():
        yield streaming_config.to_proto()
        async for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    try:
        responses = client.streaming_recognize(generate_requests())
        for response in responses:
            yield StreamingRecognitionResponse.from_proto(response)
    except GoogleAPIError as e:
        print(f"Google Cloud Speech-to-Text API Error: {e}")
