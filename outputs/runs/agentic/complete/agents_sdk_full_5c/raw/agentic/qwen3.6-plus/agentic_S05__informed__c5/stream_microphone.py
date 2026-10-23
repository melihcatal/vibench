"""Streams microphone audio and yields interim transcripts via Google Cloud Speech-to-Text streaming API."""

import queue
import threading
from typing import Generator, AsyncGenerator, Iterator
import pyaudio
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client, build_recognizer_path
from speech_models import StreamingSpeechResult, normalize_recognition_result, AudioChunk


MICROPHONE_SAMPLE_RATE = 16000
MICROPHONE_CHUNK_DURATION_MS = 200


def _audio_bytes_iterator(audio_queue: queue.Queue) -> Iterator[bytes]:
    """Yield audio bytes from a queue until a sentinel None is received."""
    while True:
        chunk = audio_queue.get()
        if chunk is None:
            break
        yield chunk


def _read_microphone_loop(audio_queue: queue.Queue, stop_event: threading.Event) -> None:
    """Continuously read from the microphone and put chunks into the queue."""
    pa = pyaudio.PyAudio()
    frames_per_buffer = int(MICROPHONE_SAMPLE_RATE * MICROPHONE_CHUNK_DURATION_MS / 1000)
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=MICROPHONE_SAMPLE_RATE,
        input=True,
        frames_per_buffer=frames_per_buffer,
    )
    try:
        while not stop_event.is_set():
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            audio_queue.put(data)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        audio_queue.put(None)


def stream_microphone(
    project_id: str,
    language_code: str = "en-US",
) -> Generator[StreamingSpeechResult, None, None]:
    """
    Stream microphone audio to Google Cloud Speech-to-Text and yield interim/final transcripts.

    Uses google-cloud-speech SDK streaming_recognize method with speech.googleapis.com endpoint.
    Model: latest_long via google-cloud-speech v2.
    """
    recognizer = build_recognizer_path(project_id=project_id)
    client = get_speech_client()
    audio_queue: queue.Queue = queue.Queue()
    stop_event = threading.Event()

    mic_thread = threading.Thread(
        target=_read_microphone_loop,
        args=(audio_queue, stop_event),
        daemon=True,
    )
    mic_thread.start()

    def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=recognizer,
            streaming_config=cloud_speech.StreamingRecognitionConfig(
                config=cloud_speech.RecognitionConfig(
                    language_codes=[language_code],
                    model="latest_long",
                    automatic_punctuation=True,
                    enable_word_time_offsets=True,
                    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
                ),
            ),
        )
        for audio_bytes in _audio_bytes_iterator(audio_queue):
            yield cloud_speech.StreamingRecognizeRequest(audio=audio_bytes)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        for result in response.results:
            normalized = normalize_recognition_result(result)
            yield normalized


async def stream_microphone_async(
    project_id: str,
    language_code: str = "en-US",
) -> AsyncGenerator[StreamingSpeechResult, None]:
    """
    Async version that streams microphone audio to Google Cloud Speech-to-Text.

    Uses google-cloud-speech SDK with speech.googleapis.com endpoint.
    """
    import asyncio
    recognizer = build_recognizer_path(project_id=project_id)
    client = get_speech_client()
    audio_queue: queue.Queue = queue.Queue()
    stop_event = threading.Event()

    mic_thread = threading.Thread(
        target=_read_microphone_loop,
        args=(audio_queue, stop_event),
        daemon=True,
    )
    mic_thread.start()

    async def async_request_generator():
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=recognizer,
            streaming_config=cloud_speech.StreamingRecognitionConfig(
                config=cloud_speech.RecognitionConfig(
                    language_codes=[language_code],
                    model="latest_long",
                    automatic_punctuation=True,
                    enable_word_time_offsets=True,
                    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
                ),
            ),
        )
        while True:
            chunk = await asyncio.get_event_loop().run_in_executor(None, audio_queue.get)
            if chunk is None:
                break
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=async_request_generator())

    for response in responses:
        for result in response.results:
            normalized = normalize_recognition_result(result)
            yield normalized

    stop_event.set()
    mic_thread.join(timeout=5)
