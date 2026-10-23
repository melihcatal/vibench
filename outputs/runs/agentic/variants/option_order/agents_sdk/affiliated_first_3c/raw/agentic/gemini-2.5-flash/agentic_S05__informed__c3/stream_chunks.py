from google.cloud import speech
import asyncio

async def stream_audio_chunks(audio_chunks_async_generator, language_code: str = "en-US"):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Assuming LINEAR16, adjust if different
        sample_rate_hertz=16000, # Assuming 16kHz, adjust if different
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    async def request_generator():
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests_iterator = request_generator() # This is an async generator, but `streaming_recognize` expects a synchronous iterator
    # To bridge the gap for demonstration, we will collect chunks first. In a real scenario, you'd feed them as they arrive.
    # For a truly async stream, you'd likely need to manage threads or an alternative client implementation.
    # For the purpose of this example, we'll make a simplification for the `client.streaming_recognize` call.

    # In a real-world async scenario, you would manage the async generator in a separate task and feed the results
    # into a queue that a synchronous generator can consume for the `client.streaming_recognize` method.
    # For this demonstration, we'll create a simple synchronous iterable from the async generator.
    # A more robust solution would involve a producer-consumer pattern with an asyncio.Queue.
    all_chunks = []
    async for chunk in audio_chunks_async_generator:
        all_chunks.append(chunk)

    def sync_generator():
        for chunk in all_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(streaming_config, sync_generator())

    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        yield transcript, result.is_final
