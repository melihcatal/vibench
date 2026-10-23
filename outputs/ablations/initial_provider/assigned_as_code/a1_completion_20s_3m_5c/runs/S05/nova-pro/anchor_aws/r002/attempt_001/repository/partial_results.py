import asyncio

from amazon_transcribe.client import TranscribeStreamingClient

async def partial_results(payload, config=None):
    config = config or {}
    client = TranscribeStreamingClient(region=config.get("region") or "us-east-1")
    stream = await client.start_stream_transcription(
        language_code=payload["language_code"], media_sample_rate_hz=payload["sample_rate_hz"], media_encoding="pcm")

    async def send_audio():
        try:
            for chunk in payload["audio_chunks"]:
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
        finally:
            await stream.input_stream.end_stream()

    sender = asyncio.create_task(send_audio())
    try:
        async for event in stream.output_stream:
            for result in event.transcript.results:
                if result.alternatives:
                    yield {"text": result.alternatives[0].transcript, "is_final": not result.is_partial}
        await sender
    finally:
        sender.cancel()
        await asyncio.gather(sender, return_exceptions=True)