import asyncio
from google.cloud.speech import StreamingRecognizeRequest
from speech_client import get_speech_client, get_streaming_config
from speech_models import CHUNK_SIZE

# In a real application, this would come from a file, a network socket, etc.
async def dummy_async_audio_generator():
    """A dummy async generator that yields silent audio chunks."""
    num_chunks = 50  # 5 seconds of audio
    for i in range(num_chunks):
        await asyncio.sleep(0.1)
        yield bytes(CHUNK_SIZE)
    print("Audio stream finished.")

async def stream_from_async_chunks(async_audio_generator):
    """
    Streams audio from an async generator of chunks and yields final transcripts.
    """
    client = get_speech_client()
    streaming_config = get_streaming_config()

    async def request_generator():
        async for chunk in async_audio_generator:
            yield StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(
        config=streaming_config,
        requests=request_generator(),
    )

    async for response in responses:
        for result in response.results:
            if result.is_final:
                yield result.alternatives[0].transcript

async def main():
    print("Starting streaming from async chunks...")
    audio_source = dummy_async_audio_generator()
    async for final_transcript in stream_from_async_chunks(audio_source):
        print(f"Transcript: {final_transcript}")

if __name__ == "__main__":
    asyncio.run(main())
