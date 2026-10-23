import asyncio
from speech_client import get_speech_client
from google.cloud.speech_v1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognizeRequest,
)


async def async_audio_generator():
    for _ in range(5):
        await asyncio.sleep(0.5)
        yield b"\x00" * 3200


async def stream_with_language_settings():
    client = get_speech_client()

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="es-ES",
        enable_automatic_punctuation=True,
    )

    streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

    async def request_generator():
        async for chunk in async_audio_generator():
            yield StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(
        config=streaming_config,
        requests=request_generator(),
    )

    async for response in responses:
        for result in response.results:
            if result.alternatives:
                print(f"Transcript (es-ES): {result.alternatives[0].transcript}")


if __name__ == "__main__":
    asyncio.run(stream_with_language_settings())
