import asyncio
import os
import queue
import threading

import aiohttp
import sounddevice as sd


OPENAI_REALTIME_API_URL = "https://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"


class MicrophoneTranscriptStreamer:
    def __init__(self, sample_rate: int = 16000, channels: int = 1, blocksize: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.blocksize = blocksize
        self._audio_queue: queue.Queue[bytes] = queue.Queue()
        self._stop_event = threading.Event()

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            pass
        self._audio_queue.put(bytes(indata))

    async def stream(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "OpenAI-Beta": "realtime=v1",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(OPENAI_REALTIME_API_URL) as ws_response:
                ws = ws_response._protocol._payload_writer.transport.get_extra_info("socket")
                if ws is None:
                    raise RuntimeError("Failed to establish realtime connection")

        loop = asyncio.get_running_loop()

        def capture_audio():
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                blocksize=self.blocksize,
                dtype="int16",
                callback=self._audio_callback,
            ):
                while not self._stop_event.is_set():
                    self._stop_event.wait(0.1)

        capture_thread = threading.Thread(target=capture_audio, daemon=True)
        capture_thread.start()

        while not self._stop_event.is_set():
            chunk = await loop.run_in_executor(None, self._audio_queue.get)
            if not chunk:
                continue
            transcript = chunk.decode("latin1", errors="ignore")
            yield transcript

    def stop(self):
        self._stop_event.set()


async def main():
    streamer = MicrophoneTranscriptStreamer()
    async for transcript in streamer.stream():
        print(transcript, flush=True)


if __name__ == "__main__":
    asyncio.run(main())
