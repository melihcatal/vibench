"""Stream microphone audio to Google Cloud Speech-to-Text and yield interim transcripts.

Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
SDK: google-cloud-speech (google.cloud.speech_v1p1beta1)
Audio capture: pyaudio for microphone streaming
"""

import queue
import threading
from typing import Generator

import pyaudio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import create_speech_client, build_streaming_config
from speech_models import StreamingTranscriptResult


CHUNK_SIZE = 1024
SAMPLE_RATE = 16000
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1


def _audio_generator(
    audio_queue: queue.Queue, stop_event: threading.Event
) -> Generator[bytes, None, None]:
    """Generate audio chunks from a thread-safe queue."""
    while not stop_event.is_set() or not audio_queue.empty():
        try:
            chunk = audio_queue.get(timeout=0.1)
            if chunk:
                yield chunk
        except queue.Empty:
            continue


def _capture_microphone(
    audio_queue: queue.Queue, stop_event: threading.Event, chunk_size: int = CHUNK_SIZE
) -> None:
    """Capture audio from the default microphone and push to queue."""
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=chunk_size,
    )
    try:
        while not stop_event.is_set():
            data = stream.read(chunk_size, exception_on_overflow=False)
            audio_queue.put(data)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


def stream_microphone_transcripts(
    language_code: str = "en-US",
    enable_punctuation: bool = True,
) -> Generator[StreamingTranscriptResult, None, None]:
    """Stream audio from the microphone to Google Cloud Speech-to-Text and yield transcripts.

    Uses google-cloud-speech SDK to connect to speech.googleapis.com.
    Yields interim and final StreamingTranscriptResult objects.

    Provider: Google Cloud Speech-to-Text
    Model: default (can be 'command_and_search', 'phone_call', 'video', etc.)
    """
    client = create_speech_client()
    streaming_config = build_streaming_config(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        model="default",
        enable_interim_results=True,
    )

    audio_queue: queue.Queue = queue.Queue()
    stop_event = threading.Event()

    capture_thread = threading.Thread(
        target=_capture_microphone, args=(audio_queue, stop_event), daemon=True
    )
    capture_thread.start()

    try:
        requests = _audio_generator(audio_queue, stop_event)
        responses = client.streaming_recognize(
            config=streaming_config,
            requests=requests,
        )

        for response in responses:
            if not response.results:
                continue
            for result in response.results:
                transcript_result = StreamingTranscriptResult.from_google_result(result)
                yield transcript_result
    finally:
        stop_event.set()
        capture_thread.join(timeout=2.0)


if __name__ == "__main__":
    print("Streaming microphone audio to Google Cloud Speech-to-Text...")
    for result in stream_microphone_transcripts():
        tag = "FINAL" if result.is_final else "INTERIM"
        print(f"[{tag}] {result.transcript} (confidence: {result.confidence:.2f})")
