import asyncio
from google.cloud import speech
from speech_client import get_async_speech_client

RATE = 16000
CHUNK = int(RATE / 10)


async def dummy_audio_stream():
    for _ in range(15):
        await asyncio.sleep(0.1)
        yield bytes(CHUNK)


async def stream_with_language_settings(language_code="es-US"):
    """
    Starts a streaming recognizer with specific language and punctuation settings.
    """
    client = get_async_speech_client()

    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(config=recognition_config)

    async def request_generator():
        async for chunk in dummy_audio_stream():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print(f"Starting streaming with language: {language_code} and punctuation enabled.")
    responses = await client.streaming_recognize(
        config=streaming_config,
        requests=request_generator(),
    )

    final_transcript = ""
    async for response in responses:
        result = response.results[0]
        if result.is_final:
            final_transcript += result.alternatives[0].transcript

    print(f"Received final transcript: {final_transcript}")
    return final_transcript


if __name__ == "__main__":
    # Example for Spanish
    asyncio.run(stream_with_language_settings(language_code="es-ES"))
    # Example for German
    asyncio.run(stream_with_language_settings(language_code="de-DE"))
