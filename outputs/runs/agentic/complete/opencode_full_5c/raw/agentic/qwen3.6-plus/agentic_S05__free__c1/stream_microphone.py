import asyncio
import audioop
from typing import AsyncIterator

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_client import SpeechConfig, build_speech_client, build_recognition_config
from speech_models import (
    StreamingResult,
    normalize_streaming_result,
    build_streaming_event,
    StreamingEvent,
)


CHUNK_SIZE = 3200
SAMPLE_RATE = 16000


def get_microphone_stream():
    import pyaudio

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )
    return p, stream


async def stream_microphone(
    config: SpeechConfig | None = None,
    duration_seconds: float | None = None,
) -> AsyncIterator[StreamingEvent]:
    cfg = config or SpeechConfig()
    client = build_speech_client(cfg)
    recognition_config = build_recognition_config(cfg)

    request_iter = _microphone_request_generator(recognition_config, duration_seconds)
    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config
    )

    requests = (
        cloud_speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        if i == 0
        else cloud_speech.StreamingRecognizeRequest(audio=r)
        for i, r in enumerate(request_iter)
    )

    responses = client.streaming_recognize(requests=requests)

    for response in responses:
        for result in response.results:
            normalized = normalize_streaming_result(result)
            event_type = "final" if normalized.is_final else "interim"
            yield build_streaming_event(event_type=event_type, result=normalized)


async def _microphone_request_generator(recognition_config, duration_seconds=None):
    import time

    p, audio_stream = get_microphone_stream()
    try:
        start_time = time.time()
        while True:
            if duration_seconds and (time.time() - start_time) >= duration_seconds:
                break
            chunk = audio_stream.read(CHUNK_SIZE, exception_on_overflow=False)
            resampled, _ = audioop.ratecv(chunk, 2, 1, SAMPLE_RATE, SAMPLE_RATE, None)
            yield resampled
            await asyncio.sleep(0)
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
