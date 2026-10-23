import asyncio
from google.cloud import speech

async def stream_audio_chunks(audio_chunks_async_generator):
    """
    Streams audio chunks from an async source to Google Cloud Speech-to-Text
    and yields interim transcripts.
    Args:
        audio_chunks_async_generator: An async generator that yields audio chunks (bytes).
    """
    client = speech.SpeechClient()

    # Configure the streaming request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        # Optional: Enable interim results
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # Create a generator for audio content
    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print("Streaming audio chunks to Google Cloud Speech-to-Text...")
    requests = request_generator()
    responses = client.streaming_recognize(requests)

    try:
        async for response in responses:
            if not response.results:
                continue

            for result in response.results:
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript
                if result.is_final:
                    yield transcript
                else:
                    yield f"[Partial] {transcript}"
    except Exception as e:
        print(f"Error during streaming: {e}")

if __name__ == "__main__":
    # Example usage: Simulate an async audio chunk generator
    async def mock_audio_chunk_generator():
        for i in range(5):
            # Simulate 1 second of silent audio (adjust as needed)
            yield b'\x00' * 32000  # 16000 samples/sec * 2 bytes/sample = 32000 bytes/sec
            await asyncio.sleep(1)
        print("Mock audio stream ended.")

    async def main():
        print("Starting mock audio streaming...")
        async for transcript in stream_audio_chunks(mock_audio_chunk_generator()):
            print(f"Received transcript: {transcript}")

    asyncio.run(main())
