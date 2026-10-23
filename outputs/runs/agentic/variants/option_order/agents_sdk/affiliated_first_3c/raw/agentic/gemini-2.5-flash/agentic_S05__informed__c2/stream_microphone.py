import asyncio
import io
import os
from google.cloud import speech

# Audio recording parameters
RATE = 16000
CHUNK = 1024

class MicrophoneStream:
    """Opens a recording stream as a generator yielding chunks of audio data."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = asyncio.Queue()
        self.closed = True

    async def __aenter__(self):
        # Import pyaudio locally to avoid issues if not installed
        import pyaudio
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

    async def __aexit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put_nowait(None)  # Signal the generator to terminate
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream into the buffer."""
        self._buff.put_nowait(in_data)
        return None, pyaudio.paContinue

    async def generator(self):
        while not self.closed:
            chunk = await self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buff.get_nowait()
                    if chunk is None:
                        break
                    data.append(chunk)
                except asyncio.QueueEmpty:
                    break
            yield b''.join(data)

async def stream_microphone_audio(language_code: str = "en-US"):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    async with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            async for content in audio_generator
        )

        responses = client.streaming_recognize(config=streaming_config, requests=requests)

        async for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            if result.is_final:
                yield f"Final: {transcript}"
            else:
                yield f"Interim: {transcript}"

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
        print("Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"")
    else:
        print("Listening for speech... Press Ctrl+C to stop.")
        try:
            async for transcript in stream_microphone_audio():
                print(transcript)
        except KeyboardInterrupt:
            print("\nStopping...")
        except Exception as e:
            print(f"An error occurred: {e}")
