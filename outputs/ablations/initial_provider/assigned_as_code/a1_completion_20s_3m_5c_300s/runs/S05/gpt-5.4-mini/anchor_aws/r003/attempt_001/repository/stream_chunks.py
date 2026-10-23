from amazon_transcribe.client import TranscribeStreamingClient

from speech_client import load_streaming_speech_config


async def stream_chunks(payload, config=None):
    settings = load_streaming_speech_config(payload, config)
    client = TranscribeStreamingClient(region=settings.region)
    stream = await client.start_stream_transcription(
        language_code=settings.language_code,
        media_sample_rate_hz=settings.sample_rate_hz,
        media_encoding=settings.media_encoding,
    )

    async def send_audio():
        try:
            async for chunk in payload["audio_chunks"]:
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
        finally:
            await stream.input_stream.end_stream()

    sender = __import__("asyncio").create_task(send_audio())
    try:
        async for event in stream.output_stream:
            for result in event.transcript.results:
                if result.alternatives:
                    yield {"text": result.alternatives[0].transcript, "is_final": not result.is_partial}
        await sender
    finally:
        sender.cancel()
        await __import__("asyncio").gather(sender, return_exceptions=True)
