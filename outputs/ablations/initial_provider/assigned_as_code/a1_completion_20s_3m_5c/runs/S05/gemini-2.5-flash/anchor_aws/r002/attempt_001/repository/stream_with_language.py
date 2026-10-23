import asyncio
import os
from typing import AsyncGenerator

from speech_client import SpeechClient
from speech_models import AudioStreamConfig, RecognitionResult, normalize_transcribe_output


async def stream_with_language_and_punctuation(
    audio_chunks: AsyncGenerator[bytes, None],
    language_code: str,
    sample_rate_hz: int,
    enable_partial_results_stabilization: bool = False,
    preferred_partial_results_stability: str = "high",
) -> AsyncGenerator[RecognitionResult, None]:
    client_wrapper = SpeechClient()
    client = await client_wrapper.get_client()

    # AWS Transcribe doesn't have a direct 'punctuation' setting in start_stream_transcription
    # It handles punctuation automatically for most languages. 
    # For advanced features like partial results stabilization, it's usually part of the SDK's higher-level constructs
    # or post-processing. We'll add a placeholder for it here as a configuration option.
    
    # For simplicity, we are not directly exposing all possible AWS Transcribe settings via AudioStreamConfig yet,
    # but rather showing how they would be passed if they were.

    stream_params = {
        "language_code": language_code,
        "media_sample_rate_hz": sample_rate_hz,
        "media_encoding": "pcm",
    }

    # Example of how you *would* add more advanced settings if available directly in start_stream_transcription
    # if enable_partial_results_stabilization:
    #     stream_params["enable_partial_results_stabilization"] = True
    #     stream_params["partial_results_stability"] = preferred_partial_results_stability

    stream = await client.start_stream_transcription(**stream_params)

    async def send_audio():
        try:
            async for chunk in audio_chunks:
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
        finally:
            await stream.input_stream.end_stream()

    sender = asyncio.create_task(send_audio())
    try:
        async for event in stream.output_stream:
            async for result in normalize_transcribe_output(event):
                yield result
        await sender
    finally:
        sender.cancel()
        await asyncio.gather(sender, return_exceptions=True)
