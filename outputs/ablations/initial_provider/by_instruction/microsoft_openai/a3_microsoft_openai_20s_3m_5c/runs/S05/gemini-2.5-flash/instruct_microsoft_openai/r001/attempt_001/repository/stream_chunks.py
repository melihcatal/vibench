import asyncio
import os
from google.cloud import speech

# Google Cloud credentials are typically handled by GOOGLE_APPLICATION_CREDENTIALS
# environment variable or automatically by the client library in a GCP environment.
# For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set.

async def stream_audio_chunks(audio_chunks_async_source):
    """
    Streams audio chunks from an async source to Google Cloud Speech-to-Text
    and yields transcription responses.
    """
    client = speech.SpeechAsyncClient()

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
        yield speech.StreamingRecognizeRequest(audio_content=None, streaming_config=streaming_config)
        async for chunk in audio_chunks_async_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print("Starting Google Cloud Speech-to-Text streaming...")
    responses = await client.streaming_recognize(requests=request_generator())

    async for response in responses:
        yield response
    print("Google Cloud Speech-to-Text streaming ended.")

# Example of an async audio chunk source (for demonstration purposes)
async def dummy_async_audio_source(num_chunks=5, chunk_size=1024):
    for i in range(num_chunks):
        # Simulate reading an audio chunk
        print(f"Producing dummy audio chunk {i+1}")
        await asyncio.sleep(0.5)  # Simulate async I/O
        yield b'\x00' * chunk_size * 2 # Dummy 16-bit audio

if __name__ == "__main__":
    async def main():
        async for response in stream_audio_chunks(dummy_async_audio_source()):
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            if result.is_final:
                print(f"Final Transcript: {transcript}")
            else:
                print(f"Partial Transcript: {transcript}")

    asyncio.run(main())
