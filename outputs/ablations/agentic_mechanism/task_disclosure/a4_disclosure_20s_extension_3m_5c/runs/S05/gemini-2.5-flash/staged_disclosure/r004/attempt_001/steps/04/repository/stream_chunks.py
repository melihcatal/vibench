import asyncio
import os
from google.cloud import speech

async def _generate_audio_chunks():
    """Simulates an asynchronous audio source by yielding dummy audio chunks."""
    # In a real application, this would read from a microphone or an audio file
    # and yield actual audio data.
    dummy_audio_data = b"\x00\x00\x00\x00" * 8000  # Simulate 1 second of silence
    for _ in range(5):  # Yield 5 chunks
        await asyncio.sleep(1)  # Simulate real-time audio
        yield dummy_audio_data

async def stream_audio_to_google_cloud():
    """Streams audio chunks to Google Cloud Speech-to-Text API."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # with the path to your service account key file.
    # For example:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

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

    # The first request must contain the streaming config
    yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)

    async for chunk in _generate_audio_chunks():
        yield speech.StreamingRecognizeRequest(audio_content=chunk)

async def main():
    """Main function to run the streaming."""
    print("Starting audio streaming to Google Cloud Speech-to-Text...")
    requests = stream_audio_to_google_cloud()
    responses = await (await speech.SpeechAsyncClient()).streaming_recognize(requests=requests)

    async for response in responses:
        # The Google Cloud provider is identifiable through the 'speech' import
        # and the use of speech.SpeechAsyncClient and related classes.
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")

if __name__ == "__main__":
    asyncio.run(main())
