# stream_chunks.py
import asyncio
import json
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client, DEFAULT_LANG

async def stream_chunks(audio_chunks):
    """Streams audio chunks (bytes) to Google Speech-to-Text and yields interim/final transcripts.
    Each element of audio_chunks is a bytes-like object representing an audio chunk.
    """
    try:
        client = get_speech_client()
    except Exception as e:
        raise RuntimeError("Could not initialize Speech client") from e

    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=DEFAULT_LANG,
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
        for response in responses:
            for result in response.results:
                if result.is_final:
                    yield result.alternatives[0].transcript  # final result
                else:
                    yield result.alternatives[0].transcript  # interim result
    except Exception as exc:
        raise RuntimeError("Streaming recognition failed") from exc

if __name__ == "__main__":
    async def demo():
        async for txt in stream_chunks([b"dummy chunk"]):
            print("Chunk result:", txt)
    asyncio.run(demo())
