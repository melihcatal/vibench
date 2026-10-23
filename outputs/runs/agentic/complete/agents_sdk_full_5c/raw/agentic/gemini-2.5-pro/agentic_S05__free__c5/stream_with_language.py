import asyncio
from google.cloud.speech import StreamingRecognizeRequest
from speech_client import get_speech_client, get_streaming_config
from speech_models import CHUNK_SIZE

async def dummy_audio_source():
    """Yields silent audio chunks for demonstration."""
    for _ in range(50): # 5 seconds of silence
        await asyncio.sleep(0.1)
        yield bytes(CHUNK_SIZE * 2)

async def recognize_with_settings(language_code: str, enable_punctuation: bool):
    """
    Starts a streaming recognizer with specific language and punctuation settings.
    """
    print(f"Starting recognizer for language '{language_code}' with punctuation: {enable_punctuation}")
    client = get_speech_client()
    streaming_config = get_streaming_config(
        language_code=language_code,
        punctuation=enable_punctuation
    )

    audio_generator = dummy_audio_source()
    requests = (StreamingRecognizeRequest(audio_content=chunk) async for chunk in audio_generator)

    responses = client.streaming_recognize(streaming_config, requests)

    final_transcript = ""
    async for response in responses:
        for result in response.results:
            if result.is_final:
                final_transcript += result.alternatives[0].transcript
    
    return final_transcript.strip()


async def main():
    # Example for Spanish with automatic punctuation
    transcript_es = await recognize_with_settings(
        language_code="es-ES",
        enable_punctuation=True
    )
    print(f"Spanish transcript: {transcript_es or 'No speech detected.'}")
    
    # Example for Japanese without automatic punctuation
    transcript_ja = await recognize_with_settings(
        language_code="ja-JP",
        enable_punctuation=False
    )
    print(f"Japanese transcript: {transcript_ja or 'No speech detected.'}")


if __name__ == "__main__":
    asyncio.run(main())
