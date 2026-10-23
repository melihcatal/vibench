import pyaudio
from google.cloud import speech
from speech_client import get_speech_client

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream:
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._audio_interface.terminate()

    def generator(self):
        while True:
            data = self._audio_stream.read(self._chunk, exception_on_overflow=False)
            if not data:
                break
            yield data


def stream_microphone():
    client = get_speech_client()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )
        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            yield response
