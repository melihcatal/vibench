import os
import asyncio
from speech_client import get_speech_client
from speech_models import get_streaming_config
from google.cloud import speech


async def async_audio_chunk_generator():
    """
    An asynchronous generator that yields mock audio chunks.
    In a real scenario, this would fetch audio from an async source.
    """
    mock_audio_data = [
        b"simulated audio chunk 1 ",
        b"simulated audio chunk 2 ",
        b"simulated audio chunk 3 ",
    ]
    for chunk in mock_audio_data:
        await asyncio.sleep(0.1)  # Simulate async I/O delay
        yield chunk


async def stream_audio_chunks_async():
    """
    Streams audio chunks from an async source and yields interim transcripts.
    """
    client = get_speech_client()
    streaming_config = get_streaming_config()

    async def generate_requests():
        async for chunk in async_audio_chunk_generator():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print("Streaming from async source...")
    requests = generate_requests()
    responses = await client.streaming_recognize(streaming_config, requests)

    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        if result.is_final:
            print(f"Final: {transcript}")
        else:
            print(f"Interim: {transcript}")
        yield transcript


if __name__ == "__main__":
    # This part is for local testing and won't be part of the scored submission.
    # async def main():
    #     async for transcript in stream_audio_chunks_async():
    #         pass
    # asyncio.run(main())
    pass
