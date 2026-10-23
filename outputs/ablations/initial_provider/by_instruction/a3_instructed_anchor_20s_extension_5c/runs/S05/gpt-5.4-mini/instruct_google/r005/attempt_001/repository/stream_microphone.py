import os
from typing import Iterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import build_client, load_config, streaming_config


def microphone_audio_stream() -> Iterator[bytes]:
    try:
        import pyaudio
    except Exception as exc:
        raise RuntimeError("pyaudio is required for microphone streaming") from exc

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    try:
        while True:
            yield stream.read(1024, exception_on_overflow=False)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


def _requests() -> Iterator[speech.StreamingRecognizeRequest]:
    for chunk in microphone_audio_stream():
        yield speech.StreamingRecognizeRequest(audio_content=chunk)


def stream_microphone() -> Iterator[str]:
    client = build_client()
    config = load_config()
    responses = client.streaming_recognize(streaming_config(config), _requests())
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript


def main() -> None:
    for transcript in stream_microphone():
        print(transcript)


if __name__ == "__main__":
    main()
