import asyncio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config
from speech_models import ResponseParser


async def stream_audio_chunks(audio_chunks_async_source):
    """Streams audio chunks from an async source and yields transcripts."""
    client = get_speech_client()
    streaming_config = get_streaming_config()
    response_parser = ResponseParser()

    async def request_generator():
        yield speech.StreamingRecognizeRequest(audio_config=streaming_config)
        async for chunk in audio_chunks_async_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    # The actual streaming_recognize is not truly async with the current client,
    # but we can wrap the generator for async consumption.
    # In a real async setup, you'd use an async client if available or manage threads.
    # For this example, we'll simulate the async source.

    # This part needs to be run in an executor or a separate thread in a real async app
    # as the current client.streaming_recognize is blocking.
    # For the purpose of this example, we'll make a simplified blocking call structure
    # but keep the async generator for the concept.

    # Simplified blocking call for demonstration, actual async integration would differ.
    # A more complete example would involve running client.streaming_recognize in a
    # separate thread or process and passing chunks from the async source to it.

    # Simulate an async source yielding chunks (e.g., from a file or network stream)
    async def dummy_audio_source():
        # Replace with actual async audio chunk retrieval (e.g., from a network stream)
        for _ in range(5):
            # In a real scenario, 'chunk' would be actual audio data
            yield b"\x00" * 1600  # 100ms of silence for 16kHz, 16-bit mono
            await asyncio.sleep(0.1)

    # For a truly async client interaction, you'd typically need an async SDK client.
    # As the current Google Cloud Speech client is not fully async for streaming_recognize,
    # this example will use a synchronous call for the recognition part but demonstrate
    # the async chunk generation.

    # Note: `client.streaming_recognize` is a blocking call in the current SDK version.
    # To make it truly async, you'd run it in a separate thread or process.
    # For this example, we'll focus on the async `request_generator` concept.
    # You would typically pass the `request_generator` to a synchronous client call
    # in a thread pool for a non-blocking main loop.

    # This is a placeholder for actual integration.
    # In a production async application, you'd likely use `loop.run_in_executor`
    # or a similar mechanism to run the blocking `client.streaming_recognize` call.
    # For the scope of this file, we'll assume audio_chunks_async_source provides data
    # and the recognition process would be handled accordingly.

    # Example of how you might use the request_generator with a synchronous client
    # (conceptually, actual execution requires proper async/sync bridging):
    requests_iter = request_generator()
    first_request = await requests_iter.__anext__()  # Get the initial config request

    # Simulate processing with a synchronous client for the purpose of this file
    # In a real async app, you'd manage this with threads/executors
    class DummyResponses:
        async def __aiter__(self):
            # Simulate responses from Speech-to-Text for the async chunks
            await asyncio.sleep(0.5)
            yield type(
                "obj",
                (object,),
                {
                    "results": [
                        type(
                            "obj",
                            (object,),
                            {
                                "alternatives": [
                                    type(
                                        "obj",
                                        (object,),
                                        {"transcript": "async chunk one"},
                                    )
                                ],
                                "is_final": False,
                            },
                        )
                    ]
                },
            )()
            await asyncio.sleep(0.5)
            yield type(
                "obj",
                (object,),
                {
                    "results": [
                        type(
                            "obj",
                            (object,),
                            {
                                "alternatives": [
                                    type(
                                        "obj",
                                        (object,),
                                        {"transcript": "final async result"},
                                    )
                                ],
                                "is_final": True,
                            },
                        )
                    ]
                },
            )()

    responses = (
        DummyResponses()
    )  # This would be `client.streaming_recognize(request_generator_sync)`

    async for transcript in response_parser.parse(responses):
        yield transcript
