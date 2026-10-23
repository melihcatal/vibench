import os
import queue
from typing import Generator, Optional

import pyaudio
from google.cloud import speech


RATE = 16000
CHUNK = int(RATE / 10)


def _requests(audio_q: "queue.Queue[Optional[bytes]]") -> Generator[speech.StreamingRecognizeRequest, None, None]:
    while True:
        chunk = audio_q.get()
        if chunk is None:
            return
        yield speech.StreamingRecognizeRequest(audio_content=chunk)


def stream_microphone() -> Generator[str, None, None]:
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=os.getenv("SPEECH_LANGUAGE_CODE", "en-US"),
        enable_automatic_punctuation=True,
        model=os.getenv("GOOGLE_CLOUD_SPEECH_MODEL", "latest_long"),
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        single_utterance=False,
    )

    audio_q: "queue.Queue[Optional[bytes]]" = queue.Queue()
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    try:
        for _ in range(3):
            audio_q.put(stream.read(CHUNK, exception_on_overflow=False))
        responses = client.streaming_recognize(streaming_config, _requests(audio_q))
        for response in responses:
            for result in response.results:
                if result.alternatives:
                    yield result.alternatives[0].transcript
    finally:
        audio_q.put(None)
        stream.stop_stream()
        stream.close()
        pa.terminate()
