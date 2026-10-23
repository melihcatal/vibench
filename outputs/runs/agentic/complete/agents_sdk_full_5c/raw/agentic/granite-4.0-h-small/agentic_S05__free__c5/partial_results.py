# partial_results.py
import json
from typing import AsyncGenerator, Dict
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamResponseHandler

async def handle_partial_results(audio_chunks: AsyncGenerator[bytes, None]):
    """Processes streaming recognition responses, separating interim and final results.
    Yields dicts with 'interim' and 'final' keys as they become available.
    """
    client = get_speech_client()
    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
    requests = (
        types.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_chunks
    )
    try:
        responses = client.streaming_recognize(streaming_config, requests)
        handler = StreamResponseHandler()
        async for resp in responses:
            for result in resp.results:
                handler.handle(result)
                if result.is_final:
                    yield {"final": result.alternatives[0].transcript}
                else:
                    yield {"interim": result.alternatives[0].transcript}
    except Exception as exc:
        raise RuntimeError("Failed to process partial results") from exc

if __name__ == "__main__":
    async def demo():
        # Simple demo producing one chunk
        async for chunk in handle_partial_results([b"demo audio"]):
            print(chunk)
    asyncio.run(demo())
