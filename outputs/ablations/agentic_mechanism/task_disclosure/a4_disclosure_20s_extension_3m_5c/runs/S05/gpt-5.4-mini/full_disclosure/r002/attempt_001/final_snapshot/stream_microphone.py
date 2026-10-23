import asyncio
import os
import queue
import threading

import pyaudio
from google.cloud import speech


class MicrophoneStream:
    def __init__(self, rate: int = 16000, chunk: int = 1600):
        self.rate = rate
        self.chunk = chunk
        self._buff = queue.Queue()
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = None
        self.closed = True

    def __enter__(self):
        self.closed = False
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self._fill_buffer,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closed = True
        if self._audio_stream is not None:
            self._audio_stream.stop_stream()
            self._audio_stream.close()
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

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


async def stream_microphone(language_code: str = "en-US", interim_results: bool = True):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )

    loop = asyncio.get_running_loop()

    with MicrophoneStream() as mic:
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in mic.generator()
        )
        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            for result in response.results:
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    if result.is_final:
                        yield {"transcript": transcript, "final": True}
                    else:
                        yield {"transcript": transcript, "final": False}


def main():
    async def runner():
        async for item in stream_microphone(
            language_code=os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US")
        ):
            print(item["transcript"])

    asyncio.run(runner())


if __name__ == "__main__":
    main()
