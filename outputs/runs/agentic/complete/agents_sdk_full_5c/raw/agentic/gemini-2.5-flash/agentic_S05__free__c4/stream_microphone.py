import asyncio
import collections
import time

from google.cloud import speech_v1p1beta1 as speech
import pyaudio

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream:
    """Opens a recording stream as a generator yielding audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = collections.deque()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.clear()
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.append(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            if self._buff:
                yield self._buff.popleft()
            else:
                # Wait for more data if the buffer is empty
                time.sleep(0.01)

async def stream_microphone_audio(client: speech.SpeechClient, config: speech.RecognitionConfig):
    """
    Streams audio from the microphone to Google Cloud Speech-to-Text API
    and yields interim transcripts.
    """
    audio_generator = None
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            # The first alternative is the most likely one for a given result.
            transcript = result.alternatives[0].transcript
            is_final = result.is_final
            yield transcript, is_final

if __name__ == '__main__':
    # Example usage:
    # This requires `pyaudio` to be installed.
    # pip install pyaudio
    #
    # And Google Cloud credentials.
    #
    # client = speech.SpeechClient()
    # config = speech.RecognitionConfig(
    #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #     sample_rate_hertz=RATE,
    #     language_code="en-US",
    # )
    #
    # async def main():
    #     async for transcript, is_final in stream_microphone_audio(client, config):
    #         print(f"Interim: {transcript}" if not is_final else f"Final: {transcript}")
    #
    # asyncio.run(main())
    pass
