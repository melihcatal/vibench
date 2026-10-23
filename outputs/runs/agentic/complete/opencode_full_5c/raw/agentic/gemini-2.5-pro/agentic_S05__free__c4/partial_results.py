import asyncio
from google.cloud import speech
from speech_client import get_async_speech_client
from speech_models import StreamingRecognitionResult

RATE = 16000
CHUNK = int(RATE / 10)


async def dummy_audio_stream():
    """Simulates an asynchronous audio stream."""
    for _ in range(20):  # Simulate 2 seconds of audio
        yield bytes(CHUNK)
        await asyncio.sleep(0.1)


async def handle_partial_results():
    """Demonstrates handling of partial and final results from streaming speech."""
    client = get_async_speech_client()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def request_generator():
        async for chunk in dummy_audio_stream():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    streaming_responses = await client.streaming_recognize(
        config=streaming_config,
        requests=request_generator(),
    )

    async for response in streaming_responses:
        for result in response.results:
            if not result.alternatives:
                continue

            recognition_result = StreamingRecognitionResult(
                transcript=result.alternatives[0].transcript,
                is_final=result.is_final,
                stability=result.stability,
            )

            if recognition_result.is_final:
                print(
                    f"FINAL: '{recognition_result.transcript}' (Stability: {recognition_result.stability})"
                )
            else:
                print(
                    f"PARTIAL: '{recognition_result.transcript}' (Stability: {recognition_result.stability})"
                )


if __name__ == "__main__":
    asyncio.run(handle_partial_results())
