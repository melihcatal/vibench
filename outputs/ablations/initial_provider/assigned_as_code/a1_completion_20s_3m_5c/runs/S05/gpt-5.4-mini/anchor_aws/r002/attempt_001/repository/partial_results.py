from speech_client import transcribe_start_args, transcribe_streaming_client


async def partial_results(payload, config=None):
    client = transcribe_streaming_client(config)
    stream = await client.start_stream_transcription(**transcribe_start_args(payload, config))
    async for event in stream.output_stream:
        for result in event.transcript.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": not result.is_partial}
