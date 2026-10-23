from google.cloud import speech_v1p1beta1 as speech
import pyaudio
import queue
import threading
import time


class MicrophoneStream:
    """Opens a recording stream as an async generator yielding audio chunks."""

    def __init__(self, rate=16000, chunk_size=1024):
        self._rate = rate
        self._chunk_size = chunk_size
        self._buff = queue.Queue()
        self._closed = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = None

    def __enter__(self):
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk_size,
            stream_callback=self._fill_buffer,
        )
        self._closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self._closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            yield chunk
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    yield chunk
                except queue.Empty:
                    break


def stream_microphone():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        model="latest_long",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream() as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in audio_generator
        )
        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            for result in response.results:
                yield {
                    "transcript": result.alternatives[0].transcript,
                    "is_final": result.is_final,
                    "stability": result.stability,
                }
