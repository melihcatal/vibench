import asyncio
from typing import AsyncGenerator
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

from speech_client import get_google_speech_client
from speech_models import TranscriptResult

# Placeholder for an asynchronous audio chunk source
async def get_async_audio_chunks() -> AsyncGenerator[bytes, None]:
    """
    Simulates an asynchronous source of audio chunks.
    In a real application, this could be from a network stream, file, etc.
    """
    for i in range(5):
        yield b"async chunk " + str(i).encode()
        await asyncio.sleep(0.1)

async def stream_audio_chunks_google(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000
) -> AsyncGenerator[TranscriptResult, None]:
    """
    Streams audio chunks from an asynchronous source to Google Cloud Speech-to-Text
    and yields interim/final transcripts.
    """
    client = get_google_speech_client() # Google Cloud Speech client

    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True, # Example of language/punctuation setting
        model="default", # Google Cloud Speech model ID is a provider-identifying signal
        use_enhanced=True,
        interim_results=True # Enable interim results
    )

    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True # Enable interim results
    )

    # Asynchronously generate audio requests
    async def request_generator():
        yield types.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in get_async_audio_chunks():
            yield types.StreamingRecognizeRequest(audio_content=chunk)

    # This part requires a small change from synchronous examples to work with async generators correctly
    # The client.streaming_recognize method expects an iterable. For async, we need to adapt.
    # In a real async scenario with Google Cloud Python SDK, a separate library like `google-cloud-speech-async`
    # or direct gRPC async might be used, or the streaming_recognize wrapped in an executor.
    # For this example, we simulate the interaction pattern for clarity.

    requests = request_generator()
    responses = await client.streaming_recognize(requests)

    async for response in responses:
        if not response.results: # No results yet
            continue

        result = response.results[0]
        if not result.alternatives: # No alternatives yet
            continue

        transcript_alternative = result.alternatives[0]
        yield TranscriptResult(
            text=transcript_alternative.transcript,
            is_partial=not result.is_final,
            confidence=transcript_alternative.confidence
        )

if __name__ == "__main__":
    async def main():
        print("Starting Google Cloud Speech-to-Text chunk stream...")
        async for transcript_result in stream_audio_chunks_google():
            status = "(Partial)" if transcript_result.is_partial else "(Final)"
            print(f"Transcript {status}: {transcript_result.text}")
    asyncio.run(main())
