from speech_client import create_transcribe_client


async def partial_results(payload, config=None):
    config = config or {}
    client = create_transcribe_client(config)
    stream = await client.start_stream_transcription(language_code=payload["language_code"], media_sample_rate_hz=payload["sample_rate_hz"], media_encoding="pcm")
    for chunk in payload["audio_chunks"]:
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()
    async for event in stream.output_stream:
        for result in event.transcript.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": not result.is_partial}
