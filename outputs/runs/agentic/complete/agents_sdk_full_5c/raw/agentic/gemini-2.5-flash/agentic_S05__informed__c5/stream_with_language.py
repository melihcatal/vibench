import asyncio
import pyaudio
from google.cloud import speech
import os

class MicrophoneStream:
    """Opens a recording stream as a generator yielding chunks of audio data."""
    def __init__(self, rate: int, chunk_size: int):
        self._rate = rate
        self._chunk_size = chunk_size
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk_size,
            stream_callback=self._fill_buffer,
        )
        self._buff = asyncio.Queue()
        self.closed = False

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put_nowait(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get_nowait()
            if chunk is None:
                return
            yield chunk

    def __enter__(self):
        self._audio_stream.start_stream()
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put_nowait(None)
        self._audio_interface.terminate()

async def stream_with_language_and_punctuation(
    rate: int = 16000, 
    chunk_size: int = 1024, 
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = False
):
    """Starts a streaming recognizer with specified language and punctuation settings."""
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=rate,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    print(f"Listening with language '{language_code}' and automatic punctuation: {enable_automatic_punctuation}...")
    with MicrophoneStream(rate, chunk_size) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript
            if result.is_final:
                print(f"Final ({result.stability:.2f}): {transcript}")
            else:
                print(f"Interim ({result.stability:.2f}): {transcript}")

if __name__ == "__main__":
    async def main():
        print("Press Ctrl+C to stop.")
        try:
            # Example: Spanish with punctuation
            # await stream_with_language_and_punctuation(language_code="es-ES", enable_automatic_punctuation=True)
            await stream_with_language_and_punctuation(language_code="en-US", enable_automatic_punctuation=True)
        except KeyboardInterrupt:
            print("Stopped listening.")

    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your service account key file for Google Cloud Speech-to-Text.")
        print("Without credentials, the application might not function as expected.")

    asyncio.run(main())
