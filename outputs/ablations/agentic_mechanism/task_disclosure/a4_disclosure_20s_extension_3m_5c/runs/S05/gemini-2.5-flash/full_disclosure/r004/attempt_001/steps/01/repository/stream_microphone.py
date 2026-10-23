import asyncio
import collections
import queue
import sys
import os

import sounddevice as sd
from google.cloud import speech

# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

class MicrophoneStream:
    """Opens a recording stream as a generator yielding chunks of audio data."""
    def __init__(self, rate=SAMPLE_RATE, chunk_size=CHUNK_SIZE):
        self._rate = rate
        self._chunk_size = chunk_size
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = sd.InputStream(
            samplerate=self._rate,
            blocksize=self._chunk_size,
            dtype="int16",
            channels=1,
            callback=self._fill_buffer,
        )
        self._audio_interface.start()
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_interface.stop()
        self._audio_interface.close()
        self.closed = True
        # Signal the generator that the stream is closed.
        self._buff.put(None)

    def _fill_buffer(self, in_data, frames, time, status):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(bytes(in_data))

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

async def stream_microphone_transcripts(language_code: str = "en-US"):
    """Streams audio from the microphone to Google Cloud Speech-to-Text and yields interim transcripts."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.", file=sys.stderr)
        print("Please set it to the path of your Google Cloud service account key file.", file=sys.stderr)
        return

    client = speech.SpeechAsyncClient() # Google Cloud Speech-to-Text client

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code=language_code,
        # Google Cloud Speech-to-Text specific feature
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    with MicrophoneStream(SAMPLE_RATE, CHUNK_SIZE) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = await client.streaming_recognize(streaming_config, requests)

        async for response in responses:
            for result in response.results:
                if result.alternatives:
                    # Yield interim results as they become available
                    yield result.alternatives[0].transcript
