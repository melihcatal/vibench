"""
Stream microphone audio to Google Cloud Speech-to-Text and yield interim transcripts.

Continuously captures audio from the system microphone and streams it to
Google Cloud Speech-to-Text, yielding interim (partial) transcription results.

Provider: Google Cloud Speech-to-Text
SDK: google-cloud-speech
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

from __future__ import annotations

import asyncio
import queue
import threading
from typing import AsyncGenerator, Optional

import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types as speech_types

from speech_client import create_streaming_speech_client, build_streaming_config
from speech_models import extract_interim_transcript, extract_final_transcripts

# Audio capture constants
MICROPHONE_SAMPLE_RATE = 16000
MICROPHONE_CHANNELS = 1
MICROPHONE_FORMAT = pyaudio.paInt16
MICROPHONE_CHUNK_DURATION = 0.05  # seconds
MICROPHONE_CHUNK_SIZE = int(MICROPHONE_SAMPLE_RATE * MICROPHONE_CHUNK_DURATION)


def _audio_capture_worker(
    audio_queue: queue.Queue,
    stop_event: threading.Event,
    device_index: Optional[int] = None,
) -> None:
    """
    Background thread worker that captures microphone audio and pushes to queue.

    Args:
        audio_queue: Thread-safe queue for audio chunks.
        stop_event: Threading event to signal capture termination.
        device_index: Optional PyAudio device index for microphone selection.
    """
    pa = pyaudio.PyAudio()
    try:
        stream = pa.open(
            format=MICROPHONE_FORMAT,
            channels=MICROPHONE_CHANNELS,
            rate=MICROPHONE_SAMPLE_RATE,
            input=True,
            frames_per_buffer=MICROPHONE_CHUNK_SIZE,
            input_device_index=device_index,
        )

        while not stop_event.is_set():
            try:
                audio_data = stream.read(
                    MICROPHONE_CHUNK_SIZE, exception_on_overflow=False
                )
                audio_queue.put(audio_data)
            except OSError:
                continue

        stream.stop_stream()
        stream.close()
    finally:
        pa.terminate()
        audio_queue.put(None)  # Sentinel to signal end of audio


async def stream_microphone_audio(
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    device_index: Optional[int] = None,
) -> AsyncGenerator[dict, None]:
    """
    Stream microphone audio to Google Cloud Speech-to-Text and yield interim transcripts.

    Captures audio from the default microphone (or specified device), streams it
    to Google Cloud Speech-to-Text API, and yields both interim and final
    transcription results.

    Args:
        language_code: BCP-47 language code for recognition.
        enable_punctuation: Whether to enable automatic punctuation.
        device_index: Optional PyAudio device index for microphone selection.

    Yields:
        Dict with keys:
            - 'type': 'interim' or 'final'
            - 'text': Transcribed text
            - 'confidence': Confidence score (0.0-1.0)
    """
    config = build_streaming_config(
        language_code=language_code,
        sample_rate_hertz=MICROPHONE_SAMPLE_RATE,
        encoding=speech_types.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=enable_punctuation,
        interim_results=True,
    )

    client = create_streaming_speech_client()
    audio_queue: queue.Queue = queue.Queue()
    stop_event = threading.Event()

    capture_thread = threading.Thread(
        target=_audio_capture_worker,
        args=(audio_queue, stop_event, device_index),
        daemon=True,
    )
    capture_thread.start()

    try:

        def request_generator():
            yield speech_types.StreamingRecognizeRequest(streaming_config=config)
            while True:
                chunk = audio_queue.get()
                if chunk is None:
                    break
                yield speech_types.StreamingRecognizeRequest(audio_content=chunk)

        responses = client.streaming_recognize(config=request_generator())

        for response in responses:
            interim_text = extract_interim_transcript(response)
            if interim_text:
                yield {
                    "type": "interim",
                    "text": interim_text,
                    "confidence": 0.0,
                }

            final_texts = extract_final_transcripts(response)
            for final_text in final_texts:
                for result in response.results:
                    if result.is_final and result.alternatives:
                        yield {
                            "type": "final",
                            "text": final_text,
                            "confidence": result.alternatives[0].confidence,
                        }
                        break

    except Exception as e:
        yield {
            "type": "error",
            "text": "",
            "confidence": 0.0,
            "error": str(e),
        }
    finally:
        stop_event.set()
        capture_thread.join(timeout=5.0)
