import asyncio
import pyaudio
import wave
from speech_client import get_speech_client
from speech_models import AudioConfig, StreamingRecognitionConfig


class MicrophoneStream:
    def __init__(self, rate=16000, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            frames_per_buffer=chunk,
            stream_callback=self._fill_buffer,
        )
        self._buff = asyncio.Queue()
        self.closed = False

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
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
                        return
                    data.append(chunk)
                except asyncio.QueueEmpty:
                    break
            yield b"".join(data)

    def close(self):
        self.closed = True
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._buff.put_nowait(None)
        self._audio_interface.terminate()


async def stream_microphone_and_transcribe():
    client = get_speech_client()

    config = StreamingRecognitionConfig(
        encoding="LINEAR16",
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        interim_results=True,
    )

    stream = MicrophoneStream()

    try:
        responses = client.streaming_recognize(config, stream.generator())

        async for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript

            if result.is_final:
                print(f"Final: {transcript}")
                yield {"text": transcript, "is_final": True}
            else:
                print(f"Interim: {transcript}")
                yield {"text": transcript, "is_final": False}

    finally:
        stream.close()


async def main():
    async for transcript in stream_microphone_and_transcribe():
        pass


if __name__ == "__main__":
    asyncio.run(main())
