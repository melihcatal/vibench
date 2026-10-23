import asyncio
import os
from google.cloud import speech

async def stream_audio_chunks(audio_chunks_generator):
    """Streams audio chunks from an async generator to Google Cloud Speech-to-Text."""

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

    # In a real application, audio_chunks_generator would yield actual audio bytes.
    # For this example, we'll simulate it.
    async def generate_requests():
        async for chunk in audio_chunks_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    requests = generate_requests()
    responses = client.streaming_recognize(streaming_config, requests)

    print("Listening for audio...")
    async for response in responses:
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")

async def example_audio_generator():
    """A dummy async generator that yields example audio chunks."""
    # In a real scenario, this would be reading from a microphone or an audio file.
    # For demonstration, we yield empty bytes.
    for i in range(3):
        print(f"Yielding chunk {i+1}")
        await asyncio.sleep(1) # Simulate delay in receiving audio
        yield b"" # Replace with actual audio bytes

async def main():
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your Google Cloud service account key file to run this example.")
        print("For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"")
        return

    await stream_audio_chunks(example_audio_generator())

if __name__ == "__main__":
    asyncio.run(main())
