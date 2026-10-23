from google.cloud import speech_v1p1beta1 as speech
import asyncio

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

async def stream_audio_chunks(audio_chunks_source):
    """Streams audio chunks from an asynchronous source to the Google Cloud Speech-to-Text API.

    Args:
        audio_chunks_source: An async generator or queue yielding audio chunks (bytes).

    Yields:
        Google Cloud Speech-to-Text recognition responses.
    """
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    async def request_generator():
        async for chunk in audio_chunks_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    # In a real scenario, the `audio_chunks_source` would be populated by an async process
    # For this example, we'll use a mock async generator.
    class MockAsyncAudioSource:
        async def __aiter__(self):
            for _ in range(5):
                # Simulate receiving audio chunks
                await asyncio.sleep(0.1)
                yield b'\x00' * CHUNK # Yielding empty bytes for simulation

    # The actual call would be:
    # responses = client.streaming_recognize(streaming_config, request_generator())
    # async for response in responses:
    #     yield response

    # Simulate responses for now
    class MockResponse:
        def __init__(self, transcript, is_final):
            self.results = [MockResult(transcript, is_final)]

    class MockResult:
        def __init__(self, transcript, is_final):
            self.alternatives = [MockAlternative(transcript)]
            self.is_final = is_final

    class MockAlternative:
        def __init__(self, transcript):
            self.transcript = transcript

    mock_responses = [
        MockResponse("async stream", False),
        MockResponse("async stream processing", False),
        MockResponse("async stream processing complete", True),
    ]

    for response in mock_responses:
        yield response
