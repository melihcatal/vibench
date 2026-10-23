import os
import asyncio
import pyaudio
from dashscope import SpeechSynthesizer, SpeechRecognizer
from speech_client import get_dashscope_client
from speech_models import TranscriptEvent

class MicrophoneStream:
    def __init__(self, rate=16000, chunk=1024):
        self._rate = rate
        self._chunk = chunk
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = None

    def __enter__(self):
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        return self

    def __exit__(self, type, value, traceback):
        if self._audio_stream:
            self._audio_stream.stop_stream()
            self._audio_stream.close()
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buffer_queue.put_nowait(in_data)
        return (None, pyaudio.paContinue)

    async def generator(self):
        self._buffer_queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        while True:
            data = await self._buffer_queue.get()
            yield data

async def stream_microphone():
    client = get_dashscope_client()
    recognizer = SpeechRecognizer(model="paraformer-realtime-v1", format="pcm", sample_rate=16000, callback=handle_result)
    microphone = MicrophoneStream()
    
    async with microphone as stream:
        async for chunk in stream.generator():
            recognizer.stream_send(chunk)
            await asyncio.sleep(0)
    recognizer.stream_close()

def handle_result(result):
    event = TranscriptEvent(
        text=result.get("text", ""),
        is_final=result.get("is_final", False),
        timestamp=result.get("timestamp", 0)
    )
    print(f"Transcript: {event.text} (Final: {event.is_final})")

if __name__ == "__main__":
    asyncio.run(stream_microphone())