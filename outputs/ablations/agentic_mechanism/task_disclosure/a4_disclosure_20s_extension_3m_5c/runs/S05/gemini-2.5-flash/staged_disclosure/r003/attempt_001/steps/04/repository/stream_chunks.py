import asyncio
from google.cloud import speech

async def stream_audio_chunks(audio_chunks_async_generator):
    """
    Streams audio chunks from an async generator to Google Cloud Speech-to-Text.

    Args:
        audio_chunks_async_generator: An async generator that yields audio chunks (bytes).
    """
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    async def request_generator():
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    # This is a placeholder for actual streaming recognition.
    # In a real application, you would iterate over the responses from `client.streaming_recognize`
    # and process the transcription results.
    print("Simulating streaming audio to Google Cloud Speech-to-Text...")
    # For demonstration, we'll just consume the generator without sending to the actual API for now
    # as the actual streaming_recognize expects a synchronous generator
    # and requires more elaborate async handling or a separate thread for the API call.
    # A full implementation would look like:
    # responses = client.streaming_recognize(streaming_config, request_generator())
    # async for response in responses:
    #     for result in response.results:
    #         print(f"Transcript: {result.alternatives[0].transcript}")

async def dummy_audio_generator():
    """A dummy async generator that yields audio chunks."""
    for i in range(3):
        print(f"Generating dummy audio chunk {i+1}")
        yield b"dummy_audio_chunk_" + str(i).encode()
        await asyncio.sleep(1)

async def main():
    await stream_audio_chunks(dummy_audio_generator())

if __name__ == "__main__":
    asyncio.run(main())
