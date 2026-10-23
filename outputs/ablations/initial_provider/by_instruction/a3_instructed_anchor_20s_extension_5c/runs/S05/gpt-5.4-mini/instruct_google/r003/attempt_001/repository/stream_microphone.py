import queue
from typing import Iterator

import pyaudio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import SpeechConfig, create_speech_client, create_streaming_config
from speech_models import normalize_text


RATE = SpeechConfig().sample_rate_hertz
CHUNK = int(RATE / 10)


def microphone_audio() -> Iterator[bytes]:
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
    try:
        while True:
            yield stream.read(CHUNK, exception_on_overflow=False)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone() -> Iterator[str]:
    client = create_speech_client()
    config = create_streaming_config()

    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in microphone_audio())
    for response in client.streaming_recognize(config=config, requests=requests):
        for result in response.results:
            if result.alternatives:
                yield normalize_text(result.alternatives[0].transcript)


if __name__ == "__main__":
    for transcript in stream_microphone():
        print(transcript)
