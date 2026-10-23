import collections
import queue
import threading

from google.cloud import speech

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class StreamClient:
    """
    Client for Google Cloud Speech-to-Text streaming recognition.
    """

    def __init__(self, language_code: str = "en-US"):
        self.language_code = language_code
        self.client = speech.SpeechClient()
        self.buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.closed = True
        self.buff.put(None)

    def _generator(self):
        while not self.closed:
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        break
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b"".join(data)

    def listen_stream(self):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=self.language_code,
        )
        streaming_config = speech.StreamingRecognitionConfig(
            config=config, interim_results=True
        )

        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in self._generator()
        )
        responses = self.client.streaming_recognize(streaming_config, requests)
        return responses

    def put(self, audio_chunk: bytes):
        self.buff.put(audio_chunk)
