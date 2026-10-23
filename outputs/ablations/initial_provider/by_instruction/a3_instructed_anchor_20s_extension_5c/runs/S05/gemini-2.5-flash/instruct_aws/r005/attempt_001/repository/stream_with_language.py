import asyncio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import SpeechClient
from speech_models import AudioChunk, TranscriptResult

# This function re-uses the core logic from stream_chunks.py but emphasizes
# the configuration of language and punctuation settings.
async def stream_with_language_settings(
    audio_chunk_generator,
    language_code: str = "en-US", # Google Cloud Speech-to-Text model identification signal: 'language_code'
    enable_automatic_punctuation: bool = True,
    # Additional settings can be passed, e.g., enable_word_time_offsets, use_enhanced, model
):
    client = SpeechClient().get_google_speech_client()

    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        # You can specify a model, e.g., model="phone_call" or model="video"
        # model="default",
        # use_enhanced=True,
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    async def request_generator():
        yield types.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunk_generator:
            if isinstance(chunk, AudioChunk):
                yield types.StreamingRecognizeRequest(audio_content=chunk.chunk_bytes)
            else:
                yield types.StreamingRecognizeRequest(audio_content=chunk)

    requests = request_generator()
    responses = client.streaming_recognize(requests)

    print(f"Starting Google Cloud Speech-to-Text stream with language='{language_code}' and punctuation={'enabled' if enable_automatic_punctuation else 'disabled'}.")
    try:
        async for response in responses:
            if not response.results:
                continue

            for result in response.results:
                is_partial = not result.is_final
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    confidence = result.alternatives[0].confidence
                    yield TranscriptResult(
                        transcript=transcript,
                        is_partial=is_partial,
                        confidence=confidence,
                        language_code=language_code
                    )

    except Exception as e:
        print(f"Error during streaming: {e}")

# Example usage (simulated audio chunk source from stream_chunks.py)
async def simulated_audio_source(num_chunks: int = 5):
    print("Simulating audio chunk generation for language settings demo...")
    for i in range(num_chunks):
        chunk_data = b'\x00' * 16000 * 2
        yield AudioChunk(chunk_bytes=chunk_data, sequence_number=i)
        await asyncio.sleep(0.5)
    yield AudioChunk(chunk_bytes=b'', sequence_number=num_chunks, is_last_chunk=True)


if __name__ == "__main__":
    async def main():
        print("Demonstrating streaming with specific language and punctuation settings.")
        # Example: German with punctuation
        print("\n--- Streaming in German (de-DE) ---")
        async for transcript_result in stream_with_language_settings(
            simulated_audio_source(num_chunks=3),
            language_code="de-DE",
            enable_automatic_punctuation=True
        ):
            print(f"[{'PARTIAL' if transcript_result.is_partial else 'FINAL'}] [{transcript_result.language_code}] {transcript_result.transcript}")

        # Example: Spanish without punctuation
        print("\n--- Streaming in Spanish (es-ES) without punctuation ---")
        async for transcript_result in stream_with_language_settings(
            simulated_audio_source(num_chunks=3),
            language_code="es-ES",
            enable_automatic_punctuation=False
        ):
            print(f"[{'PARTIAL' if transcript_result.is_partial else 'FINAL'}] [{transcript_result.language_code}] {transcript_result.transcript}")

    asyncio.run(main())
