import asyncio
import os
import json
from typing import Dict

# Third‑party provider: Google Cloud Speech‑to‑Text (Streaming)
# The provider is identified by the SDK import and the hostname used in the client.
from google.cloud import speech_v1p1beta1 as speech

# Environment variable expected: GOOGLE_APPLICATION_CREDENTIALS

# Helper that mirrors the same microphone generator used elsewhere
async def _microphone_generator(sample_rate_hz: int = 16000, chunk_size: int = 1024) -> Dict:
    """Yield raw PCM audio chunks from the default microphone."""
    import sounddevice as sd
    stream = sd.InputStream(samplerate=sample_rate_hz, channels=1, dtype='int16', callback=sd.CallbackParameters)
    stream.start()
    while True:
        data = stream.read(chunk_size)
        yield data.tobytes()  # type: ignore
    stream.stop()

async def stream_with_language(
    language_code: str = "en-US",
    sample_rate_hz: int = 16000,
) -> Dict:
    """Start a streaming recognizer with explicit language and punctuation settings.
    Returns a sample response payload (demonstrating how to capture the result)."""
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
    requests = [speech.StreamingRecognizeRequest(streaming_config=streaming_config)]
    async for audio_chunk in _microphone_generator(sample_rate_hz=sample_rate_hz):
        requests.append(speech.StreamingRecognizeRequest(audio_content=audio_chunk))
        await asyncio.sleep(0.01)
    async for resp in client.streaming_recognize(requests):
        # Return the first response received (for demo purposes)
        return resp

if __name__ == "__main__":
    result = asyncio.run(stream_with_language())
    print(json.dumps(result.to_dict(), indent=2))
