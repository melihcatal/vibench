import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
import asyncio

async def stream_audio_chunks(audio_chunks_async_generator):
    """Streams audio chunks from an async source to Google Speech-to-Text and yields transcripts.

    Args:
        audio_chunks_async_generator: An async generator that yields audio chunks (bytes).
    """
    client = speech.SpeechClient() # Using default credentials (GOOGLE_APPLICATION_CREDENTIALS)

    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    async def request_generator():
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print("Starting chunk streaming recognition...")
    responses = await client.streaming_recognize(streaming_config, request_generator())

    # The client.streaming_recognize returns an async iterator
    async for response in responses:
        for result in response.results:
            if result.is_final:
                print(f"Final: {result.alternatives[0].transcript}")
            else:
                print(f"Interim: {result.alternatives[0].transcript}")
            yield result.alternatives[0].transcript

async def _dummy_audio_chunk_source():
    """A dummy async generator for testing purposes, yields empty bytes."""
    for _ in range(5):
        print("Yielding dummy chunk...")
        yield b'' # In a real scenario, this would be actual audio data
        await asyncio.sleep(1)

if __name__ == "__main__":
    # To run this, ensure GOOGLE_APPLICATION_CREDENTIALS is set.
    # This example uses a dummy audio source.
    print("This script demonstrates streaming from async chunks. Using dummy data for now.")
    async def main():
        async for transcript in stream_audio_chunks(_dummy_audio_chunk_source()):
            pass # Process transcripts here
    
    # asyncio.run(main()) # Uncomment to run with dummy data
    print("Uncomment asyncio.run(main()) to test with dummy chunks.")
