from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
from speech_models import get_recognition_config

async def start_streaming_recognizer_with_settings(
    audio_chunks_async_gen,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    sample_rate_hertz: int = 16000,
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
):
    """
    Starts a streaming speech recognizer with specified language and punctuation settings.

    Args:
        audio_chunks_async_gen: An async generator that yields audio chunks (bytes).
        language_code: The BCP-47 language code, e.g., "en-US", "es-ES".
        enable_automatic_punctuation: Whether to enable automatic punctuation in the transcript.
        sample_rate_hertz: The sample rate of the audio in Hertz.
        encoding: The audio encoding type.

    Yields:
        Tuples of (transcript, is_final) for each meaningful result.
    """
    client = get_speech_client()
    config = get_recognition_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        sample_rate_hertz=sample_rate_hertz,
        encoding=encoding,
    )

    async def request_generator():
        async for chunk in audio_chunks_async_gen:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    responses = await client.streaming_recognize(streaming_config, request_generator())

    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        is_final = result.is_final
        yield transcript, is_final

if __name__ == '__main__':
    # Example usage:
    # import asyncio
    #
    # async def dummy_audio_source():
    #     # Simulate receiving audio chunks
    #     for i in range(3):
    #         await asyncio.sleep(1) # Simulate network delay or processing
    #         yield b'dummy_audio_data_' + str(i).encode()
    #
    # async def main():
    #     print("Starting streaming recognizer with custom settings...")
    #     async for transcript, is_final in start_streaming_recognizer_with_settings(
    #         dummy_audio_source(),
    #         language_code="es-ES",
    #         enable_automatic_punctuation=True,
    #     ):
    #         print(f"[{'FINAL' if is_final else 'PARTIAL'}] {transcript}")
    #
    # asyncio.run(main())
    pass
