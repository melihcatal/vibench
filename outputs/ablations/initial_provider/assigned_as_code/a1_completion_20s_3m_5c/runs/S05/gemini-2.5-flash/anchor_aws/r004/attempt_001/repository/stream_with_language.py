import asyncio

import boto3

from amazon_transcribe.client import TranscribeStreamingClient

async def stream_with_language(payload, config=None):
    config = config or {}
    client = TranscribeStreamingClient(region=config.get("region") or boto3.Session().region_name or "us-east-1")

    start_stream_kwargs = {
        "language_code": payload["language_code"],
        "media_sample_rate_hz": payload["sample_rate_hz"],
        "media_encoding": "pcm",
    }

    if "enable_partial_results_stabilization" in payload:
        start_stream_kwargs["enable_partial_results_stabilization"] = payload["enable_partial_results_stabilization"]
        start_stream_kwargs["partial_results_stabilization_strategy"] = payload.get(
            "partial_results_stabilization_strategy", "latest"
        )
    if "enable_automatic_punctuation" in payload:
        start_stream_kwargs["enable_automatic_punctuation"] = payload["enable_automatic_punctuation"]

    stream = await client.start_stream_transcription(**start_stream_kwargs)

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
