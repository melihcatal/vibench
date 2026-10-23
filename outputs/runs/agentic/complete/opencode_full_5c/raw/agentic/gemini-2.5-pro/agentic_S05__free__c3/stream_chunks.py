import asyncio
from speech_client import get_speech_client, get_streaming_config
from google.cloud.speech_v1.types import StreamingRecognizeRequest


async def async_audio_chunk_generator():
    for i in range(5):
        await asyncio.sleep(0.5)
        yield b"\x00" * 3200


async def stream_chunks():
    client = get_speech_client()
    streaming_config = get_streaming_config()

    async def request_generator():
        async for chunk in async_audio_chunk_generator():
            yield StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(
        config=streaming_config,
        requests=request_generator(),
    )

    async for response in responses:
        for result in response.results:
            if result.alternatives:
                print(f"Transcript from chunk: {result.alternatives[0].transcript}")


if __name__ == "__main__":
    asyncio.run(stream_chunks())
