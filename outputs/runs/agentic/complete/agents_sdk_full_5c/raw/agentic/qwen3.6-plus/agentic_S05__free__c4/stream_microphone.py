"""Streams microphone audio and yields interim transcripts using Google Cloud Speech-to-Text streaming API."""

import queue
import sys
import threading
from typing import Generator, Optional

import sounddevice as sd
from google.cloud import speech_v1p1beta1 as speech

from speech_client import create_streaming_recognition_config, get_speech_client
from speech_models import StreamingSpeechEvent, normalize_streaming_result, TranscriptSegment

SAMPLE_RATE = 16000
CHUNK_DURATION_MS = 200
BYTES_PER_SAMPLE = 2
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000) * BYTES_PER_SAMPLE


def _microphone_stream(
    audio_queue: queue.Queue,
    sample_rate: int = SAMPLE_RATE,
    chunk_size: int = CHUNK_SIZE,
):
    """Read audio from the default microphone and push PCM chunks into a queue.

    Uses sounddevice.InputStream to capture 16-bit LINEAR16 PCM audio for Google Cloud Speech.
    """
    def callback(indata, frames, time_info, status):
        if status:
            print(f"Microphone status: {status}", file=sys.stderr)
        audio_queue.put(bytes(indata))

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
        blocksize=int(chunk_size // BYTES_PER_SAMPLE),
        callback=callback,
    ):
        while True:
            try:
                chunk = audio_queue.get(timeout=1.0)
                yield chunk
            except queue.Empty:
                break


def stream_microphone_audio(
    language_code: str = "en-US",
    sample_rate_hertz: int = SAMPLE_RATE,
    enable_automatic_punctuation: bool = True,
    timeout_seconds: Optional[float] = None,
) -> Generator[StreamingSpeechEvent, None, None]:
    """Stream audio from the microphone and yield interim and final transcript events.

    Uses google.cloud.speech_v1p1beta1.SpeechClient.streaming_recognize with the
    'latest_long' model for continuous Google Cloud Speech-to-Text transcription.
    """
    audio_queue: queue.Queue = queue.Queue()
    client = get_speech_client()

    streaming_config = create_streaming_recognition_config(
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model="latest_long",
    )

    def audio_generator():
        yield from _microphone_stream(audio_queue, sample_rate_hertz)

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_generator()
    )

    # Prepend config request
    config_request = speech.StreamingRecognizeRequest(
        streaming_config=streaming_config
    )

    def request_iter():
        yield config_request
        yield from requests

    try:
        responses = client.streaming_recognize(requests=request_iter())
        for response in responses:
            event = StreamingSpeechEvent()
            if response.results:
                for result in response.results:
                    segment = normalize_streaming_result(result)
                    event.segments.append(segment)
            if response.speech_event_type:
                event.raw_response = str(response.speech_event_type)
            yield event
    except Exception as exc:
        yield StreamingSpeechEvent(error=f"Google Cloud Speech streaming error: {exc}")
