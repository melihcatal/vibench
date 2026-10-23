import asyncio
from google.cloud import speech
import os

async def process_streaming_recognition_events(audio_generator):
    """Processes streaming recognition events from Google Cloud Speech-to-Text,
    handling partial and final results.
    """
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # In a real application, audio_generator would come from a microphone or file stream
    # For this example, we simulate it with a placeholder generator.
    # The client.streaming_recognize expects an iterable of requests.
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_generator())

    print("Starting streaming recognition...")
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        # Once the transcription has settled, the first result will contain the word timings
        # and confidence, and `is_final` will be set to True.
        if not response.results:
            continue

        result = response.results[0]

        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            print(f"Final Transcript: {transcript}")
            # You can perform further actions with the final transcript here
        else:
            print(f"Partial Transcript: {transcript}")
            # Display interim results to the user

async def simulate_audio_input(duration_seconds: int = 5, chunk_size: int = 1024):
    """Simulates an audio input generator yielding silent audio chunks.
    In a real scenario, this would be actual microphone or file data.
    """
    RATE = 16000 # Sample rate
    BYTES_PER_SAMPLE = 2 # 16-bit audio
    total_bytes = RATE * BYTES_PER_SAMPLE * duration_seconds
    current_bytes = 0
    while current_bytes < total_bytes:
        # Yield a chunk of silence
        chunk = b'\x00' * min(chunk_size, total_bytes - current_bytes)
        yield chunk
        current_bytes += len(chunk)
        await asyncio.sleep(chunk_size / (RATE * BYTES_PER_SAMPLE)) # Simulate real-time delay


if __name__ == "__main__":
    # To run this example, you need to provide an audio generator.
    # For a simple test, we'll use a simulated audio input.
    async def main():
        # Create an async generator for audio input
        audio_gen_func = lambda: simulate_audio_input(duration_seconds=10)
        await process_streaming_recognition_events(audio_gen_func)

    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or ensure gcloud is authenticated
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your service account key file for Google Cloud Speech-to-Text.")
        print("For now, simulating with silent audio, so no actual transcription will occur without credentials.")

    asyncio.run(main())
