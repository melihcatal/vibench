import asyncio
from speech_client import SpeechClient
from speech_models import TranscriptionResult, AudioChunk

async def stream_chunks(audio_chunks_async_iterable, language_code, sample_rate_hz, config=None):
    config = config or {}
    speech_client = SpeechClient(region=config.get("region"))
    stream = await speech_client.start_transcription_stream(language_code, sample_rate_hz)

    async def send_audio():
        try:
            async for chunk in audio_chunks_async_iterable:
                await stream.input_stream.send_audio_event(audio_chunk=chunk.content)
        finally:
            await stream.input_stream.end_stream()

    sender = asyncio.create_task(send_audio())
    try:
        async for event in stream.output_stream:
            for result in event.transcript.results:
                if result.alternatives:
                    yield TranscriptionResult(
                        text=result.alternatives[0].transcript,
                        is_final=not result.is_partial
                    )
        await sender
    finally:
        sender.cancel()
        await asyncio.gather(sender, return_exceptions=True)
