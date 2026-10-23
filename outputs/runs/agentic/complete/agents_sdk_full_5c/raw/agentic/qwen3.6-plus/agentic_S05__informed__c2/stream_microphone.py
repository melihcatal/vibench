"""
Streams microphone audio and yields interim transcripts using Google Cloud Speech-to-Text.
Captures real-time audio from a microphone device and performs streaming recognition.

Provider: Google Cloud Speech-to-Text Streaming API
SDK: google-cloud-speech
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import asyncio
import logging
from collections.abc import AsyncGenerator
from typing import Optional

import pyaudio
from google.cloud import speech_v1p1beta1 as speech

from partial_results import handle_streaming_response
from speech_client import build_streaming_config, create_speech_client
from speech_models import PartialTranscriptResult, StreamingAudioChunk

logger = logging.getLogger(__name__)

# Audio capture constants
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION_MS = 100
BYTES_PER_SAMPLE = 2
CHUNK_SIZE = int(SAMPLE_RATE * CHANNELS * CHUNK_DURATION_MS / 1000) * BYTES_PER_SAMPLE


async def microphone_audio_stream(
    device_index: Optional[int] = None,
    sample_rate: int = SAMPLE_RATE,
    chunk_size: int = CHUNK_SIZE,
    channels: int = CHANNELS,
) -> AsyncGenerator[bytes, None]:
    """
    Stream raw audio bytes from the system microphone.

    Args:
        device_index: PyAudio device index (None for default).
        sample_rate: Audio sample rate in Hz.
        chunk_size: Number of bytes per audio chunk.
        channels: Number of audio channels.

    Yields:
        Raw audio bytes from the microphone.
    """
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=chunk_size // BYTES_PER_SAMPLE,
    )

    try:
        while True:
            audio_bytes = await asyncio.to_thread(stream.read, chunk_size, exception_on_overflow=False)
            yield audio_bytes
    except GeneratorExit:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


async def stream_microphone_transcripts(
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    device_index: Optional[int] = None,
    stop_event: Optional[asyncio.Event] = None,
) -> AsyncGenerator[PartialTranscriptResult, None]:
    """
    Stream microphone audio to Google Cloud Speech and yield interim/final transcripts.

    Uses the Google Cloud Speech-to-Text streaming API via the google-cloud-speech SDK.

    Args:
        language_code: BCP-47 language code for recognition.
        enable_automatic_punctuation: Whether to enable auto-punctuation.
        device_index: PyAudio device index (None for default).
        stop_event: Optional asyncio.Event to signal stop.

    Yields:
        PartialTranscriptResult objects with interim and final transcripts.
    """
    client = create_speech_client()

    streaming_config = build_streaming_config(
        sample_rate_hertz=SAMPLE_RATE,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    async def request_generator():
        """Generate streaming requests: config followed by audio chunks."""
        config_request = speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        yield config_request

        async for audio_bytes in microphone_audio_stream(device_index=device_index):
            audio_request = speech.StreamingRecognizeRequest(audio_content=audio_bytes)
            yield audio_request
            if stop_event and stop_event.is_set():
                break

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        if stop_event and stop_event.is_set():
            break
        partial_results = handle_streaming_response(response)
        for partial in partial_results:
            yield partial
