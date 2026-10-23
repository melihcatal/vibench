import pyaudio
import queue
import threading
import time
from google.cloud import speech_v1p1beta1 as speech


class MicrophoneStream:
    def __init__(self, rate=16000, chunk_size=1024):
        self.rate = rate
        self.chunk_size = chunk_size
        self.buff = queue.Queue()
        self.closed = False
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._fill_buffer,
        )
        self.client = speech.SpeechClient()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self.buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b"".join(data)

    def close(self):
        self.closed = True
        self.buff.put(None)
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio_interface.terminate()


def stream_microphone():
    stream = MicrophoneStream()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in stream.generator()
    )

    responses = stream.client.streaming_recognize(streaming_config, requests)

    try:
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            is_final = result.is_final

            yield {
                "transcript": transcript,
                "is_final": is_final,
                "stability": result.stability if hasattr(result, "stability") else None,
                "confidence": result.alternatives[0].confidence
                if result.alternatives[0].confidence
                else None,
            }
    finally:
        stream.close()
