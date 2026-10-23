import asyncio
from typing import Optional
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


async def start_streaming_recognizer(
    audio_generator,
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    enable_word_time_offsets: bool = False,
    sample_rate: int = 16000,
    model: Optional[str] = None,
    profanity_filter: bool = False,
):
    client = get_speech_client()

    config = StreamingRecognitionConfig(
        encoding="LINEAR16",
        sample_rate_hertz=sample_rate,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        interim_results=True,
        enable_word_time_offsets=enable_word_time_offsets,
        profanity_filter=profanity_filter,
    )

    if model:
        config.model = model

    responses = client.streaming_recognize(config, audio_generator)

    return responses


async def stream_with_multilingual_support():
    client = get_speech_client()

    languages = ["en-US", "es-ES", "fr-FR", "de-DE"]

    async def mock_multilingual_audio():
        for i in range(20):
            yield b"\x00" * 1600
            await asyncio.sleep(0.05)

    for lang in languages:
        print(f"\nStarting streaming recognition for {lang}")

        config = StreamingRecognitionConfig(
            encoding="LINEAR16",
            sample_rate_hertz=16000,
            language_code=lang,
            enable_automatic_punctuation=True,
            interim_results=True,
        )

        responses = client.streaming_recognize(config, mock_multilingual_audio())

        async for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            if result.is_final:
                print(f"[{lang}] Final: {transcript}")
                break
            else:
                print(f"[{lang}] Interim: {transcript}")


async def stream_with_enhanced_model():
    client = get_speech_client()

    async def mock_audio():
        for i in range(15):
            yield b"\x00" * 3200
            await asyncio.sleep(0.1)

    config = StreamingRecognitionConfig(
        encoding="LINEAR16",
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        interim_results=True,
        model="video",  # Using enhanced model for better accuracy
    )

    responses = client.streaming_recognize(config, mock_audio())

    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        confidence = result.alternatives[0].confidence

        if result.is_final:
            print(f"Enhanced model final: {transcript} (confidence: {confidence:.2f})")
        else:
            print(f"Enhanced model interim: {transcript}")


if __name__ == "__main__":
    print("Testing multilingual streaming...")
    asyncio.run(stream_with_multilingual_support())

    print("\nTesting enhanced model streaming...")
    asyncio.run(stream_with_enhanced_model())
