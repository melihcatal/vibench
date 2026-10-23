import asyncio

# Google Cloud Speech-to-Text
from google.cloud import speech_v1p1beta1 as speech

# Helper utilities from local modules
from speech_client import get_speech_client
from speech_models import StreamingRecognizeRequest

# Configuration (could be loaded from env vars or config file)
LANGUAGE_CODE = "en-US"
SAMPLE_RATE_HZ = 16000
CHUNK_SIZE = 1024  # bytes
INTERIM_RESULTS = True

async def chunk_generator(source_async_iter):
    """Yield audio chunks from any async iterable (e.g., a network socket)."""
    async for chunk in source_async_iter:
        yield chunk

async def stream_chunks(source_async_iter):
    """Stream audio chunks to Google Cloud STT and print interim/final transcripts."""
    client = get_speech_client()
    chunk_iter = chunk_generator(source_async_iter)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE_HZ,
        language_code=LANGUAGE_CODE,
        enable_automatic_punctuation=INTERIM_RESULTS,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=INTERIM_RESULTS,
    )
    requests = [
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in chunk_iter
    ]
    async with client.streaming_recognize(streaming_config, requests) as response_stream:
        async for result in response_stream:
            if result.results:
                for r in result.results:
                    if r.alternatives:
                        transcript = r.alternatives[0].transcript
                        is_final = r.is_final
                        print(f"{"INTERIM" if not is_final else "FINAL"}: {transcript}")

# Example usage: replace `source_async_iter` with your actual async data source.
# asyncio.run(stream_chunks(async_iterable_of_audio_chunks))
