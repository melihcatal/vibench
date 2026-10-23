import asyncio
from google.cloud.speech_v1p1beta1.services.speech import SpeechAsyncClient
from google.cloud.speech_v1p1beta1.types import speech_pb2
from typing import AsyncGenerator, AsyncIterable
from speech_client import get_speech_config

async def stream_chunks(audio_chunks: AsyncIterable[bytes]) -> AsyncGenerator[str, None]:
    # Uses GOOGLE_APPLICATION_CREDENTIALS env for auth
    get_speech_config('google')  # validate config

    client = SpeechAsyncClient()

    streaming_config = speech_pb2.StreamingRecognitionConfig(
        config=speech_pb2.RecognitionConfig(
            encoding=speech_pb2.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        ),
        interim_results=True,
    )

    async def generate_requests():
        yield speech_pb2.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for audio_content in audio_chunks:
            yield speech_pb2.StreamingRecognizeRequest(audio_content=audio_content)

    stream = client.streaming_recognize(requests=generate_requests())

    async for response in stream:
        for result in response.results:
            alt = result.alternatives[0]
            transcript = alt.transcript
            marker = " (final)" if result.is_final else " (interim)"
            yield transcript + marker