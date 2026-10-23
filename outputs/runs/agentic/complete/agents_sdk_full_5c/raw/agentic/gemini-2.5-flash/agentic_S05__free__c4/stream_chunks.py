from google.cloud import speech_v1p1beta1 as speech

async def stream_audio_chunks(client: speech.SpeechClient, config: speech.RecognitionConfig, audio_chunks_async_gen):
    """
    Streams audio chunks from an asynchronous source to Google Cloud Speech-to-Text API
    and yields interim transcripts.

    Args:
        client: The Google Cloud SpeechClient instance.
        config: The RecognitionConfig for the streaming recognition.
        audio_chunks_async_gen: An async generator that yields audio chunks (bytes).
    """
    async def request_generator():
        async for chunk in audio_chunks_async_gen:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # The client.streaming_recognize method expects an iterable. For async generators,
    # we need to ensure it's awaited if it's not directly compatible. 
    # Here, we wrap it in a synchronous generator which internally awaits.
    responses = await client.streaming_recognize(streaming_config, request_generator())

    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        is_final = result.is_final
        yield transcript, is_final

if __name__ == '__main__':
    # Example usage (requires an async audio chunk source):
    # from speech_client import get_speech_client
    # from speech_models import get_default_recognition_config
    #
    # async def dummy_audio_source():
    #     # Simulate receiving audio chunks
    #     for i in range(5):
    #         await asyncio.sleep(1) # Simulate network delay or processing
    #         yield b'simulate_audio_chunk_' + str(i).encode()
    #
    # async def main():
    #     client = get_speech_client()
    #     config = get_default_recognition_config()
    #     async for transcript, is_final in stream_audio_chunks(client, config, dummy_audio_source()):
    #         print(f"Chunk Transcript: {transcript} (Final: {is_final})")
    #
    # import asyncio
    # asyncio.run(main())
    pass
