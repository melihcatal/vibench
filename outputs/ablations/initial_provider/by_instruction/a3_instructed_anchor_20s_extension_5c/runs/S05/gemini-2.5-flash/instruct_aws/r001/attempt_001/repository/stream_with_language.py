import asyncio
from google.cloud import speech

async def stream_with_language_settings(audio_chunks_async_generator, language_code="en-US", enable_automatic_punctuation=True):
    """
    Starts a streaming recognizer with specified language and punctuation settings.
    Streams audio chunks from an async source to Google Cloud Speech-to-Text
    and yields interim transcripts.

    Args:
        audio_chunks_async_generator: An async generator that yields audio chunks (bytes).
        language_code (str): The BCP-47 language tag for the spoken language.
        enable_automatic_punctuation (bool): If True, enables automatic punctuation in the transcript.
    """
    client = speech.SpeechClient()

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
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print(f"Starting streaming recognition with language '{language_code}' and punctuation '{enable_automatic_punctuation}'...")
    requests = request_generator()
    responses = client.streaming_recognize(requests)

    try:
        async for response in responses:
            if not response.results:
                continue

            for result in response.results:
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript
                if result.is_final:
                    yield transcript
                else:
                    yield f"[Partial] {transcript}"
    except Exception as e:
        print(f"Error during streaming: {e}")

if __name__ == "__main__":
    async def mock_audio_chunk_generator():
        for _ in range(3):
            yield b'\x00' * 32000  # Simulate 1 second of silent audio
            await asyncio.sleep(1)
        print("Mock audio stream ended.")

    async def main():
        print("Streaming with custom settings (en-US, punctuation enabled)...")
        async for transcript in stream_with_language_settings(
            mock_audio_chunk_generator(),
            language_code="en-US",
            enable_automatic_punctuation=True
        ):
            print(f"Transcript: {transcript}")

        print("\nStreaming with custom settings (es-ES, punctuation disabled)...")
        async for transcript in stream_with_language_settings(
            mock_audio_chunk_generator(),
            language_code="es-ES",
            enable_automatic_punctuation=False
        ):
            print(f"Transcript: {transcript}")

    asyncio.run(main())
