import asyncio

from speech_client import build_stream_request, create_transcribe_client
from speech_models import normalize_chunk


async def stream_chunks(payload, config=None):
    config = config or {}
    request = build_stream_request(payload, config)
    client = create_transcribe_client(config)
    stream = await client.start_stream_transcription(language_code=request.language_code, media_sample_rate_hz=request.sample_rate_hz, media_encoding="pcm")

    async def send_audio():
        try:
            for chunk in request.audio_chunks:
                await stream.input_stream.send_audio_event(audio_chunk=normalize_chunk(chunk))
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
