import asyncio
import os
from google.cloud import speech

# This file demonstrates streaming audio chunks from an asynchronous source
# to Google Cloud Speech-to-Text API.

async def async_audio_chunk_generator():
    """Simulates an asynchronous source yielding audio chunks."""
    # In a real application, this could be reading from a file, a network stream,
    # or a microphone captured by an async library.
    print("Simulating async audio chunk generation...")
    for i in range(5):
        # Simulate a small audio chunk (e.g., 1 second of silence, 16kHz, 16-bit mono)
        # A real audio chunk would contain actual spoken words.
        chunk = b'\x00' * 16000 * 2 # 1 second of dummy audio
        yield chunk
        await asyncio.sleep(1) # Simulate delay in receiving chunks
    print("Finished simulating async audio chunks.")

async def stream_audio_chunks():
    client = speech.SpeechClient()

    # Configuration for the streaming recognition request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    # Create an asynchronous generator for the audio content
    audio_generator = async_audio_chunk_generator()

    async def request_generator():
        async for chunk in audio_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print("Starting streaming recognition with Google Cloud Speech-to-Text...")
    try:
        # The `stream` method expects an async generator for requests
        responses = client.streaming_recognize(config=streaming_config, requests=request_generator())

        async for response in responses:
            if not response.results:
                continue

            for result in response.results:
                if result.is_final:
                    yield f"Final: {result.alternatives[0].transcript}"
                else:
                    yield f"Partial: {result.alternatives[0].transcript}"
    except Exception as e:
        print(f"Error during streaming: {e}")

if __name__ == "__main__":
    # To run this example, ensure you have Google Cloud credentials configured.
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    async def main():
        async for transcript in stream_audio_chunks():
            print(transcript)

    asyncio.run(main())
