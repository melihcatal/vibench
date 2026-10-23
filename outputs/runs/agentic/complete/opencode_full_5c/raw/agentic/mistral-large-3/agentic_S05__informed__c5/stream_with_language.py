import os
from typing import AsyncGenerator, Dict, Any
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


async def stream_with_language(
    audio_chunks: AsyncGenerator[bytes, None],
    language_code: str = "en-US",
    enable_punctuation: bool = True,
) -> AsyncGenerator[Dict[str, Any], None]:
    """Starts a streaming recognizer with language and punctuation settings using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    config = StreamingRecognitionConfig(
        language_code=language_code,
        interim_results=True,
        enable_automatic_punctuation=enable_punctuation,
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
