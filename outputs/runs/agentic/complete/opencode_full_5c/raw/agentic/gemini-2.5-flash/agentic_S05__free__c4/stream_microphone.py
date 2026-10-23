import asyncio
import os
import queue
import sys

from google.cloud import speech_v1p1beta1 as speech

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream:
    """Opens a recording stream as a generator yielding chunks of audio data."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        # Placeholder for actual microphone setup, as direct microphone access isn't available in this environment.
        # In a real scenario, this would use an audio library like PyAudio.
        # For demonstration, we'll simulate an audio stream.
        print(
            "Simulating microphone stream. In a real application, PyAudio would be used here."
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.closed = True
        # Signal the generator to terminate
        self._buff.put(None)

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                break
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        break
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


async def stream_microphone_audio(language_code: str = "en-US"):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        model="default",
        use_enhanced=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    # In a real application, you'd integrate with an audio library like PyAudio here
    # For this example, we'll yield empty bytes to simulate continuous streaming
    # and allow the client to process.
    async def request_generator():
        while True:
            # Simulate silence or empty audio for demonstration
            # In a real scenario, this would read from the microphone stream
            yield speech.StreamingRecognizeRequest(audio_content=b"")
            await asyncio.sleep(CHUNK / RATE)  # Simulate chunk interval

    requests = request_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield transcript, result.is_final
