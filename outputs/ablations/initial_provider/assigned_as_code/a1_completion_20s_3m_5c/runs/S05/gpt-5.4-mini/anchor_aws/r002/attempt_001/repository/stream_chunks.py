from speech_client import transcribe_start_args, transcribe_streaming_client


async def stream_chunks(payload, config=None):
    client = transcribe_streaming_client(config)
    stream = await client.start_stream_transcription(**transcribe_start_args(payload, config))
    async for chunk in payload["audio_chunks"]:
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
        yield chunk
    await stream.input_stream.end_stream()
