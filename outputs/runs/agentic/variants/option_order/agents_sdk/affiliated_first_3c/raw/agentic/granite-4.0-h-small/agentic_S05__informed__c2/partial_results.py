import asyncio
from typing import AsyncGenerator, Dict

# Third‑party provider: Google Cloud Speech‑to‑Text (Streaming)
# The SDK import signals the provider
from google.cloud import speech_v1p1beta1 as speech

# Environment variable for authentication (GOOGLE_APPLICATION_CREDENTIALS) is expected.

def _microphone_generator(sample_rate_hz: int = 16000, chunk_size: int = 1024) -> AsyncGenerator[bytes, None]:
    """Yield raw PCM audio chunks from the default microphone (Linux/macOS)."""
    import sounddevice as sd
    stream = sd.InputStream(samplerate=sample_rate_hz, channels=1, dtype='int16', callback=sd.CallbackParameters)
    stream.start()
    while True:
        data = stream.read(chunk_size)
        yield data.tobytes()  # type: ignore
    stream.stop()

async def _handle_results(
    response: speech.StreamingRecognizeResponse,
) -> None:
    """Process a full response from the streaming API, emitting partial and final results."""
    for result in response.results:
        if result.is_final:
            # Final transcription line
            print("[FINAL] ", result.alternatives[0].transcript)
        else:
            # Interim / partial transcription
            print("[INTERIM] ", result.alternatives[0].transcript, end='\\r')
    return None

async def partial_results(
    language_code: str = "en-US",
    sample_rate_hz: int = 16000,
) -> AsyncGenerator[Dict, None]:
    """Connect to the Speech‑to‑Text streaming endpoint, feed microphone audio, and emit results as they arrive."""
    client = speech.StreamingSpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hz,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
    # Initial request with only the config (no audio yet)
    requests = [speech.StreamingRecognizeRequest(streaming_config=streaming_config)]
    # Add microphone chunks
    async for audio_chunk in _microphone_generator(sample_rate_hz=sample_rate_hz):
        requests.append(speech.StreamingRecognizeRequest(audio_content=audio_chunk))
        await asyncio.sleep(0.01)  # brief yield to keep the event loop active
    # Stream the requests to the service using async iterator
    async for resp in client.streaming_recognize(requests):
        yield from _handle_results(resp)

if __name__ == "__main__":
    # Simple demo: run the partial‑result recognizer and print all output
    asyncio.run(partial_results())
