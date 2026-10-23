import asyncio
from google.cloud import speech
from speech_client import get_async_speech_client

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


async def async_audio_generator():
    """A dummy async generator for audio chunks."""
    for i in range(10):
        await asyncio.sleep(0.1)
        yield bytes(CHUNK)


async def stream_from_chunks():
    """Streams audio from an async generator and returns the final transcript."""
    client = get_async_speech_client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(config=config)

    async def request_generator():
        async for chunk in async_audio_generator():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(streaming_config, request_generator())

    final_transcript = ""
    async for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        if result.is_final:
            final_transcript += result.alternatives[0].transcript

    return final_transcript


if __name__ == "__main__":
    final_result = asyncio.run(stream_from_chunks())
    print(f"Final transcript from chunks: {final_result}")
