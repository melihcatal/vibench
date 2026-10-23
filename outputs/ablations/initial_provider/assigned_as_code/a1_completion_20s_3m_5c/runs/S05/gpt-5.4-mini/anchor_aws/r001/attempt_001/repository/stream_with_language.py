import asyncio

from speech_client import create_transcribe_client


async def stream_with_language(payload, config=None):
    config = config or {}
    client = create_transcribe_client(config)
    stream = await client.start_stream_transcription(language_code=payload.get("language_code", "en-US"), media_sample_rate_hz=payload["sample_rate_hz"], media_encoding="pcm", enable_partial_results_stabilization=True, show_speaker_label=False, vocabulary_name=payload.get("vocabulary_name"), language_model_name=payload.get("language_model_name"))

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
                    yield {"text": result.alternatives[0].transcript, "is_final": not result.is_partial, "language_code": payload.get("language_code", "en-US")}
        await sender
    finally:
        sender.cancel()
        await asyncio.gather(sender, return_exceptions=True)
