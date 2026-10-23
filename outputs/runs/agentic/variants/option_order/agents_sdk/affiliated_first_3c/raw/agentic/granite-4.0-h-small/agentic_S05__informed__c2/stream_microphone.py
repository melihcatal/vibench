import asyncio
import audioop
import json
from typing import AsyncGenerator

# Third‑party provider: Google Cloud Speech‑to‑Text (Streaming)
from google.cloud import speech_v1p1beta1 as speech

# Environment variable used for authentication
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

def _microphone_generator(sample_rate_hz: int = 16000, chunk_size: int = 1024) -> AsyncGenerator[bytes, None]:
    """Yield raw PCM audio chunks from the default microphone.
    Uses the `audioop` module to read in 16‑bit mono audio.
    """
    import sounddevice as sd
    stream = sd.InputStream(samplerate=sample_rate_hz, channels=1, dtype='int16', callback=sd.CallbackParameters)
    stream.start()
    while True:
        data = stream.read(chunk_size)
        yield data.tobytes()  # type: ignore
    stream.stop()

async def stream_microphone(
    language_code: str = "en-US",
    sample_rate_hz: int = 16000,
) -> AsyncGenerator[speech.StreamingRecognizeResponse, None]:
    """Open a streaming recognizer and feed microphone audio.
    Yields partial and final transcription results as they become available.
    """
    client = speech.StreamingSpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hz,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,  # receive interim partial transcripts
    )
    requests = [speech.StreamingRecognizeRequest(streaming_config=streaming_config)]
    async for audio_chunk in _microphone_generator(sample_rate_hz=sample_rate_hz):
        requests.append(speech.StreamingRecognizeRequest(audio_content=audio_chunk))
        await asyncio.sleep(0.01)  # brief yield to keep the loop responsive
    async for resp in client.streaming_recognize(requests):
        yield resp

if __name__ == "__main__":
    async for resp in stream_microphone():
        for result in resp.results:
            if result.alternatives:
                print(result.alternatives[0].transcript, end='\n' if result.is_final else '')
