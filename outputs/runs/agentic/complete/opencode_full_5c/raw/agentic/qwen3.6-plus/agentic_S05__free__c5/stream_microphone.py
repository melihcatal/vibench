import asyncio
import queue
import threading
from typing import AsyncGenerator, Optional

import pyaudio
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

from speech_client import SpeechConfig, create_speech_client, build_recognition_config
from speech_models import StreamingTranscriptEvent, normalize_streaming_event

CHUNK_DURATION_MS = 200
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16
BYTES_PER_SAMPLE = 2
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)


def _audio_generator(audio_queue: queue.Queue, stop_event: threading.Event):
    while not stop_event.is_set():
        try:
            data = audio_queue.get(timeout=0.5)
            if data is None:
                break
            yield data
        except queue.Empty:
            continue


def _capture_audio(
    audio_queue: queue.Queue,
    stop_event: threading.Event,
    sample_rate: int,
    channels: int,
    chunk_size: int,
):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=channels,
        rate=sample_rate,
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
        p.terminate()
        audio_queue.put(None)


async def stream_microphone(
    config: Optional[SpeechConfig] = None,
    sample_rate: int = SAMPLE_RATE,
    channels: int = CHANNELS,
    chunk_size: int = CHUNK_SIZE,
) -> AsyncGenerator[StreamingTranscriptEvent, None]:
    if config is None:
        config = SpeechConfig.from_env()
        config.sample_rate_hertz = sample_rate
        config.audio_channel_count = channels

    client = create_speech_client(config)
    recognition_config = build_recognition_config(config)

    audio_queue: queue.Queue = queue.Queue()
    stop_event = threading.Event()

    capture_thread = threading.Thread(
        target=_capture_audio,
        args=(audio_queue, stop_event, sample_rate, channels, chunk_size),
        daemon=True,
    )
    capture_thread.start()

    request_iter = _audio_generator(audio_queue, stop_event)

    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config,
        streaming_features=cloud_speech.StreamingRecognitionFeatures(
            enable_voice_activity_events=True,
            interim_results=True,
        ),
    )

    config_request = cloud_speech.StreamingRecognizeRequest(
        recognizer=config.recognizer_path,
        streaming_config=streaming_config,
    )

    def request_generator():
        yield config_request
        for audio_data in request_iter:
            yield cloud_speech.StreamingRecognizeRequest(audio=audio_data)

    loop = asyncio.get_event_loop()
    responses = await loop.run_in_executor(
        None, lambda: client.streaming_recognize(requests=request_generator())
    )

    try:
        for response in responses:
            event = normalize_streaming_event(response)
            if event is not None:
                yield event
    finally:
        stop_event.set()
        capture_thread.join(timeout=5)
