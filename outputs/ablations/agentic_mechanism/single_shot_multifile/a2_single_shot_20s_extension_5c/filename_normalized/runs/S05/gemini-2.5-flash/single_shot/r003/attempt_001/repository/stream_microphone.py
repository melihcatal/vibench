import asyncio
import pyaudio
import os

from google.cloud.speech_v1p1beta1 import SpeechClient
from google.cloud.speech_v1p1beta1.types import RecognitionConfig, StreamingRecognitionConfig, StreamingRecognizeRequest

from speech_client import get_speech_client, get_streaming_config
from speech_models import TranscriptResult, AudioChunk

RATE = 16000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

async def stream_microphone_audio() -> AsyncIterator[AudioChunk]:
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    try:
        while True:
            data = stream.read(CHUNK)
            yield AudioChunk(content=data, sample_rate_hertz=RATE)
            await asyncio.sleep(0.001)
    except asyncio.CancelledError:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

async def stream_microphone() -> AsyncIterator[StreamingRecognizeRequest]:
    client: SpeechClient = get_speech_client()
    
    config = get_streaming_config(language_code="en-US", enable_automatic_punctuation=True, sample_rate_hertz=RATE)
    streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

    audio_generator = stream_microphone_audio()
    
    yield StreamingRecognizeRequest(streaming_config=streaming_config)

    async for chunk in audio_generator:
        yield StreamingRecognizeRequest(audio_content=chunk.content)
