import asyncio
from google.cloud import speech

from speech_client import get_streaming_speech_client
from speech_models import StreamingRecognitionConfig


async def stream_audio_chunks(
    audio_chunks_async_generator, config: StreamingRecognitionConfig
):
    client = get_streaming_speech_client()
    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,  # Assuming 16kHz for streamed chunks
            language_code=config.language_code,
            enable_automatic_punctuation=config.enable_automatic_punctuation,
        ),
        interim_results=True,
    )

    async def generate_requests():
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests_generator = generate_requests()
    responses = client.streaming_recognize(streaming_config, requests_generator)

    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        yield result


if __name__ == "__main__":
    # Example usage:
    async def dummy_audio_source():
        # This is a placeholder for an actual async audio source
        # In a real scenario, this would read audio from a file, network, etc.
        sample_rate = 16000
        duration_seconds = 1
        num_samples = sample_rate * duration_seconds
        import array
        import random

        for _ in range(5):  # Simulate 5 chunks
            # Generate some dummy audio data (silent or noise)
            audio_data = array.array(
                "h", (random.randint(-1000, 1000) for _ in range(num_samples))
            ).tobytes()
            await asyncio.sleep(1)  # Simulate delay in receiving chunks
            yield audio_data

    async def main():
        config = StreamingRecognitionConfig(
            language_code="en-US", enable_automatic_punctuation=True
        )
        print("Starting to stream dummy audio chunks...")
        try:
            async for result in stream_audio_chunks(dummy_audio_source(), config):
                transcript = result.alternatives[0].transcript
                is_final = result.is_final
                print(f"Transcript (final={is_final}): {transcript}")
        except KeyboardInterrupt:
            print("\nStopped streaming.")

    asyncio.run(main())
