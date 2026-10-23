import asyncio

from amazon_transcribe.client import TranscribeStreamingClient

async def stream_with_language(language_code, audio_chunks, config=None):
    config = config or {}
    client = TranscribeStreamingClient(region=config.get("region") or "us-east-1")
    stream = await client.start_stream_transcription(
        language_code=language_code, media_sample_rate_hz=16000, media_encoding="pcm")
    async def send_audio():
        try:
            for chunk in audio_chunks:
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
        finally:
            await stream.input_stream.end_stream()
    sender = asyncio.create_task(send_audio())
    try:
        async for event in stream.output_stream:
            yield event
        await sender
    finally:
        sender.cancel()
        await asyncio.gather(sender, return_exceptions=True)