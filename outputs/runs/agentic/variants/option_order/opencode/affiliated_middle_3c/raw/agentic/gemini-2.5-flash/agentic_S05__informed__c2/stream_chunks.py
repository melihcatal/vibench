import asyncio
from google.cloud import speech
from speech_client import get_speech_client
from speech_models import SpeechConfig

# Audio recording parameters (dummy for this example)
RATE = 16000
CHUNK_SIZE = 3200  # Roughly 200ms of audio at 16kHz 16-bit mono


async def dummy_audio_chunk_generator():
    """A dummy async generator for audio chunks."""
    for i in range(5):
        # Simulate an audio chunk (e.g., raw bytes from a file or network)
        dummy_chunk = b"\x00" * CHUNK_SIZE
        yield dummy_chunk
        await asyncio.sleep(0.5)  # Simulate async I/O


async def stream_audio_chunks(audio_chunk_generator):
    client = get_speech_client()
    config = SpeechConfig()

    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=config.language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=audio_config,
        interim_results=True,
    )

    async def request_generator():
        async for chunk in audio_chunk_generator:
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print("Streaming audio chunks...")
    # Note: google-cloud-speech SDK's streaming_recognize is not truly async-await friendly
    # This part would typically be adapted for a real async context or run in a separate thread.
    # For demonstration, we'll iterate over the async generator in a synchronous manner for the request creation.
    # In a real async application, you'd use client.recognize_stream which needs async iterators/generators.

    # The google-cloud-speech SDK expects a synchronous iterable for requests.
    # To bridge the async generator, we would typically run the async generator
    # in a separate thread and feed its output into a queue that a synchronous
    # iterator consumes for the streaming_recognize call.
    # For this example, we'll demonstrate the structure.

    # A more robust solution for async chunking would involve a queue and a separate thread
    # to pull from the async generator and put into the queue for the synchronous client call.
    # Since the prompt asks for a direct streaming client, we'll structure it conceptually.

    # For a truly async Google Cloud Speech streaming client, you'd typically look for
    # an async client or manage this concurrency manually.

    # Let's mock the synchronous request feeding from an async source for this example.
    # In a production scenario, you would need to adapt the async audio_chunk_generator
    # to be consumed by the synchronous `streaming_recognize` method, perhaps with a queue.

    # Simplified for demonstration purposes to show the integration point.
    requests = []
    async for chunk in audio_chunk_generator:
        requests.append(speech.StreamingRecognizeRequest(audio_content=chunk))

    responses = client.streaming_recognize(streaming_config, iter(requests))

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield {"is_final": result.is_final, "transcript": transcript}


if __name__ == "__main__":

    async def main():
        async for result in stream_audio_chunks(dummy_audio_chunk_generator()):
            print(f"Chunk Stream Result: {result}")

    asyncio.run(main())
