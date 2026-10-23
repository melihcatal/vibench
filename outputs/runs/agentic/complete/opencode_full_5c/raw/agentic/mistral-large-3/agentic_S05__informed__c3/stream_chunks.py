import asyncio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig, PartialResult, FinalResult


async def stream_chunks(audio_source):
    """Streams audio chunks from an async source and yields transcripts."""
    client = get_speech_client()
    config = StreamingRecognitionConfig(
        language_code="en-US",
        enable_automatic_punctuation=True,
        interim_results=True,
    )

    requests = (
        types.StreamingRecognizeRequest(audio_content=chunk)
        async for chunk in audio_source
    )

    streaming_config = types.StreamingRecognitionConfig(
        config=config.to_grpc(),
        interim_results=True,
    )

    responses = client.streaming_recognize(streaming_config, requests)

    async for response in responses:
        for result in response.results:
            if result.is_final:
                yield FinalResult.from_grpc(result)
            else:
                yield PartialResult.from_grpc(result)
