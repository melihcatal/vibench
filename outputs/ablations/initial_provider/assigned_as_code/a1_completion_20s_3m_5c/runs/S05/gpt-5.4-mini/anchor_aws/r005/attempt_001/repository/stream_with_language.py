import asyncio

from amazon_transcribe.client import TranscribeStreamingClient

from speech_client import build_transcribe_client, build_streaming_request


async def stream_with_language(payload, config=None):
    request = build_streaming_request(payload)
    client: TranscribeStreamingClient = build_transcribe_client(config)
    stream = await client.start_stream_transcription(
        language_code=request.language_code,
        media_sample_rate_hz=request.sample_rate_hz,
        media_encoding="pcm",
        enable_partial_results_stabilization=True,
        show_speaker_label=False,
        vocabulary_filter_method="mask" if request.enable_punctuation else None,
    )

    async def send_audio():
        try:
            for chunk in request.audio_chunks:
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
        finally:
            await stream.input_stream.end_stream()

    sender = asyncio.create_task(send_audio())
    try:
        async for event in stream.output_stream:
            for result in event.transcript.results:
                if result.alternatives:
                    yield {"text": result.alternatives[0].transcript, "is_final": not result.is_partial, "language_code": request.language_code, "punctuation": request.enable_punctuation}
        await sender
    finally:
        sender.cancel()
        await asyncio.gather(sender, return_exceptions=True)
