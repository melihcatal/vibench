import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client

# ---------------------------------------------------------------------------
# SAME-SCENARIO: stream_microphone.py                                      #
# Streams microphone audio and yields interim transcripts using Google Cloud Speech-to-Text.
# ---------------------------------------------------------------------------

# Constants
CHUNK = 1600  # 100ms of 16kHz audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

async def microphone_generator():
    """Yield audio chunks from the microphone."""
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            if data:
                yield data
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

async def run():
    client = get_speech_client()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config,
                                                         interim_results=True)
    audio_stream = microphone_generator()
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_stream
    )
    responses = client.streaming_recognize(streaming_config, requests)
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                transcript = result.alternatives[0].transcript
                is_final = result.is_final
                print(f"{transcript}{' (final)' if is_final else ''}")

if __name__ == "__main__":
    asyncio.run(run())