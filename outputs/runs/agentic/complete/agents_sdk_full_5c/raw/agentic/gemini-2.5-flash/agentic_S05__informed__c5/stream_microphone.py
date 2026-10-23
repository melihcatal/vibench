import asyncio
import pyaudio
from google.cloud import speech

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
            # Run in a separate thread to avoid blocking
            stream_callback=self._fill_buffer,
        )
        self._buff = asyncio.Queue()
        self.closed = False

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect audio data from the stream into the buffer."""
        self._buff.put_nowait(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Generates audio chunks from the microphone."""
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

async def stream_microphone_audio(rate: int = 16000, chunk_size: int = 1024):
    """Streams microphone audio to Google Cloud Speech-to-Text and yields interim transcripts."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=rate,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

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
                yield f"Final: {transcript}"
            else:
                yield f"Interim: {transcript}"

if __name__ == "__main__":
    async def main():
        print("Listening... Press Ctrl+C to stop.")
        try:
            async for transcript in stream_microphone_audio():
                print(transcript)
        except KeyboardInterrupt:
            print("Stopped listening.")
    asyncio.run(main())
