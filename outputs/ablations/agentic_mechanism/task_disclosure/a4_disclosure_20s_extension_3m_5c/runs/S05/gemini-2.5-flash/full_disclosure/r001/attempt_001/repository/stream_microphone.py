import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks

class MicrophoneStream:
    """Opens a recording stream as an iterable object."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a buffer to store audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of data.
            # If the stream is closed, this will stop blocking and return None.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever is on the queue.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response is provided
    by the API.

    When the transcription response comes, print the transcript. If `is_final` is True,
    the transcription has been finalized and the result will not change. If `is_final`
    is False, it is an interim result that may be overwritten by a newer response.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        # Display interim results, overwrite the previous line if non-final.
        # If the previous result was longer than this one, we need to overwrite the
        # remainder of the previous line with spaces, otherwise the old text will
        # linger on the screen.
        if result.is_final:
            print(transcript + "\n")
            num_chars_printed = 0
        else:
            overwrite_chars = " " * (num_chars_printed - len(transcript))
            print(transcript + overwrite_chars + "\r", end="")
            num_chars_printed = len(transcript)


def stream_microphone_audio():
    """Streams audio from the microphone to the Google Cloud Speech-to-Text API and prints interim transcripts."""
    language_code = "en-US"  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            types.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, create the generator that feeds audio into the API and combines
        # responses with an audio stream.
        listen_print_loop(responses)

if __name__ == "__main__":
    stream_microphone_audio()
