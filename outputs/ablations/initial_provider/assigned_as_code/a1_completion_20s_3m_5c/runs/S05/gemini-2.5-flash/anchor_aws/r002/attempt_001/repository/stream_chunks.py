import asyncio
from typing import AsyncGenerator

from speech_client import SpeechClient
from speech_models import AudioStreamConfig, RecognitionResult, normalize_transcribe_output


async def stream_chunks(audio_chunks: AsyncGenerator[bytes, None], config: AudioStreamConfig) -> AsyncGenerator[RecognitionResult, None]:
    client_wrapper = SpeechClient()
    client = await client_wrapper.get_client()

    stream = await client.start_stream_transcription(
        language_code=config.language_code,
        media_sample_rate_hz=config.sample_rate_hz,
        media_encoding=config.media_encoding
    )

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
