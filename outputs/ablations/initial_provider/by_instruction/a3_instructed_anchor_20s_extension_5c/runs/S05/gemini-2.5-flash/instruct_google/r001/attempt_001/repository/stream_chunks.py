from typing import AsyncIterable
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig, StreamingRecognitionResponse

async def stream_audio_chunks(
    audio_chunks: AsyncIterable[bytes],
    rate: int = 16000
) -> StreamingRecognitionResponse:
    """Streams audio chunks from an async source and yields interim transcripts."""

    client = get_speech_client()

    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=rate,
        language_code="en-US",
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
