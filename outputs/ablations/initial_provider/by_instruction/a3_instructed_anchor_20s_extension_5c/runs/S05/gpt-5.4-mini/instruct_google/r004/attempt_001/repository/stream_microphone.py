import queue
from typing import Generator, Iterable, Optional

import pyaudio
from google.cloud import speech

from speech_client import build_speech_client, streaming_config
from speech_models import segment_from_google_result


def microphone_audio_chunks(rate: int = 16000, chunk_size: int = 1600) -> Generator[bytes, None, None]:
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk_size)
    try:
        while True:
            yield stream.read(chunk_size, exception_on_overflow=False)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone(language_code: str = "en-US", enable_punctuation: bool = True) -> Generator[str, None, None]:
    client = build_speech_client()
    config = streaming_config(language_code=language_code, enable_punctuation=enable_punctuation)

    def requests() -> Iterable[speech.StreamingRecognizeRequest]:
        for content in microphone_audio_chunks():
            yield speech.StreamingRecognizeRequest(audio_content=content)

    for response in client.streaming_recognize(config=config, requests=requests()):
        for result in response.results:
            segment = segment_from_google_result(result)
            if segment.text:
                yield segment.text
