import os
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = bytes()
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff += in_data
        return None, pyaudio.paContinue

    def generator(self):
        while True:
            chunk = self._buff[: self._chunk]
            self._buff = self._buff[self._chunk :]
            if not chunk:
                break
            yield chunk

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._audio_interface.terminate()


def stream_microphone():
    client = get_speech_client()
    config = StreamingRecognitionConfig(
        config=types.RecognitionConfig(
            encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            model="latest_long",
        ),
        interim_results=True,
    )

    with MicrophoneStream(rate=16000, chunk=1024) as stream:
        audio_generator = stream.generator()
        requests = (
            types.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )
        responses = client.streaming_recognize(config, requests)

        for response in responses:
            for result in response.results:
                yield {
                    "transcript": result.alternatives[0].transcript,
                    "is_final": result.is_final,
                    "stability": result.stability,
                }
