import os
import asyncio
from typing import AsyncGenerator, Dict, Any, AsyncIterable
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


async def stream_chunks(
    audio_chunks: AsyncIterable[bytes],
) -> AsyncGenerator[Dict[str, Any], None]:
    """Streams audio chunks from an async source and yields interim transcripts using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    config = StreamingRecognitionConfig(
        language_code="en-US",
        interim_results=True,
        enable_automatic_punctuation=True,
    ).to_google_config()

    requests = (
        types.StreamingRecognizeRequest(audio_content=chunk)
        async for chunk in audio_chunks
    )

    responses = await client.streaming_recognize(config, requests)
    async for response in responses:
        for result in response.results:
            yield {
                "transcript": result.alternatives[0].transcript,
                "is_final": result.is_final,
                "stability": result.stability,
            }
