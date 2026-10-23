import queue
from typing import Iterator

import pyaudio

from speech_client import build_client, default_config, streaming_config
from speech_models import event_from_result


RATE = 16000
CHUNK = int(RATE / 10)


def audio_stream() -> Iterator[bytes]:
    q = queue.Queue()
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=lambda in_data, frame_count, time_info, status: (q.put(in_data), pyaudio.paContinue)[1])
    stream.start_stream()
    try:
        while True:
            yield q.get()
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone() -> Iterator[str]:
    client = build_client()
    cfg = default_config(sample_rate_hertz=RATE)
    requests = ({"audio_content": content} for content in audio_stream())
    for response in client.streaming_recognize(streaming_config(cfg), requests):
        for result in response.results:
            event = event_from_result(result, cfg.language_code)
            if event.text:
                yield event.text
