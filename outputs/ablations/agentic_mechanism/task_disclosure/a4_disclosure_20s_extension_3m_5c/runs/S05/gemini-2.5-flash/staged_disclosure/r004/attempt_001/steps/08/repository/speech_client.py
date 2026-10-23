import os
import io

from google.cloud import speech

def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()

def get_streaming_config(
    sample_rate_hertz: int,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    """Returns a StreamingRecognitionConfig for Google Cloud Speech-to-Text."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    return streaming_config

class MicrophoneStream:
    """Opens a recording stream as a generator yielding audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = io.BytesIO()
        self.closed = True

    def __enter__(self):
        # This is a placeholder. In a real application, you would initialize an audio input stream here
        # For example, using PyAudio:
        # import pyaudio
        # self._audio_interface = pyaudio.PyAudio()
        # self._audio_stream = self._audio_interface.open(
        #     format=pyaudio.paInt16,
        #     channels=1,
        #     rate=self._rate,
        #     input=True,
        #     frames_per_buffer=self._chunk,
        #     stream_callback=self._fill_buffer,
        # )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        # Placeholder for closing the audio stream
        # self._audio_stream.stop_stream()
        # self._audio_stream.close()
        # self._audio_interface.terminate()
        self.closed = True
        self._buff.seek(0)
        self._buff.truncate(0)

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect audio data until the stream is closed."""
        self._buff.write(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.read(self._chunk)
            if chunk:
                yield chunk
            else:
                # This would typically wait for more data in a real-time stream
                pass
