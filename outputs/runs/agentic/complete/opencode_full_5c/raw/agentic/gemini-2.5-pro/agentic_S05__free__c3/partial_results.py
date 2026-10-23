import asyncio
from speech_client import get_speech_client, get_streaming_config
from speech_models import normalize_transcript_response
from google.cloud.speech_v1.types import StreamingRecognizeRequest


async def async_audio_generator():
    for i in range(10):
        await asyncio.sleep(0.2)
        yield b"\x00" * 1600


async def handle_partial_results():
    client = get_speech_client()
    streaming_config = get_streaming_config()

    async def request_generator():
        async for chunk in async_audio_generator():
            yield StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(
        config=streaming_config,
        requests=request_generator(),
    )

    async for response in responses:
        normalized_results = normalize_transcript_response(response)
        for result in normalized_results:
            if result.is_final:
                print(f"Final result: {result.transcript}")
            else:
                print(f"Partial result: {result.transcript}")


if __name__ == "__main__":
    asyncio.run(handle_partial_results())
