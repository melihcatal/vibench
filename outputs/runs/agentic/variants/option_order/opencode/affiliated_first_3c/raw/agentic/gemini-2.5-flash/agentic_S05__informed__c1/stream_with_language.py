import asyncio
from google.cloud import speech


async def mock_audio_stream():
    # Placeholder for an audio stream
    yield b"audio_data_1"
    await asyncio.sleep(0.1)
    yield b"audio_data_2"


async def stream_with_language_settings(
    client: speech.SpeechClient,
    audio_stream_iterator,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_stream_iterator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    print(
        f"Streaming with language: {language_code}, punctuation: {enable_automatic_punctuation}"
    )
    async for response in responses:
        for result in response.results:
            if result.is_final:
                print(f"Final ({language_code}): {result.alternatives[0].transcript}")
            else:
                print(f"Partial ({language_code}): {result.alternatives[0].transcript}")


if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up for authentication
    # google-cloud-speech is the SDK used
    # Cloud Speech-to-Text streaming is the service
    # The client is identified by speech.SpeechClient
    client = speech.SpeechClient()

    async def main():
        print("--- English (US) ---")
        await stream_with_language_settings(
            client,
            mock_audio_stream(),
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
        print("\n--- Spanish (Spain) ---")
        await stream_with_language_settings(
            client,
            mock_audio_stream(),
            language_code="es-ES",
            enable_automatic_punctuation=False,
        )

    asyncio.run(main())
