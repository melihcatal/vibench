import os
import asyncio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_google_speech_client, get_google_streaming_config
from speech_models import TranscriptChunk

async def stream_audio_chunks(audio_chunks_async_iter):
    client = get_google_speech_client()
    config = get_google_streaming_config("en-US")

    # The first request must contain the AudioConfig, subsequent requests must contain audio data.
    yield speech.StreamingRecognizeRequest(streaming_config=config)

    async for chunk in audio_chunks_async_iter:
        yield speech.StreamingRecognizeRequest(audio_content=chunk)

async def process_audio_chunk_stream(audio_chunks_async_iter):
    client = get_google_speech_client()
    requests_generator = stream_audio_chunks(audio_chunks_async_iter)
    recognizer_stream = client.streaming_recognize(requests=requests_generator)

    async for response in recognizer_stream:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        alternative = result.alternatives[0]
        if alternative.transcript:
            yield TranscriptChunk(
                text=alternative.transcript,
                start_time=result.result_end_time.total_seconds() - alternative.words[0].start_time.total_seconds() if alternative.words else 0.0, # Placeholder
                end_time=result.result_end_time.total_seconds(),
                is_final=result.is_final
            )
