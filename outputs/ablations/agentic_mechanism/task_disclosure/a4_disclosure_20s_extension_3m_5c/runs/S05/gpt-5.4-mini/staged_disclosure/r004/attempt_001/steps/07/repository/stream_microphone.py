import asyncio
import base64
import json
import os
import queue
import threading
from typing import AsyncIterator, Iterator, Optional

import pyaudio
import websockets


OPENAI_REALTIME_URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-mini-realtime-preview"


class MicrophoneStream:
    def __init__(self, rate: int = 24000, chunk: int = 1024) -> None:
        self.rate = rate
        self.chunk = chunk
        self._audio = pyaudio.PyAudio()
        self._buffer: "queue.Queue[Optional[bytes]]" = queue.Queue()
        self._stream = None
        self._closed = threading.Event()

    def __enter__(self) -> "MicrophoneStream":
        self._stream = self._audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self._callback,
        )
        self._stream.start_stream()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _callback(self, in_data, frame_count, time_info, status_flags):
        if not self._closed.is_set():
            self._buffer.put(in_data)
        return None, pyaudio.paContinue

    def generator(self) -> Iterator[bytes]:
        while not self._closed.is_set():
            chunk = self._buffer.get()
            if chunk is None:
                break
            yield chunk

    def close(self) -> None:
        if self._closed.is_set():
            return
        self._closed.set()
        try:
            self._buffer.put_nowait(None)
        except queue.Full:
            pass
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
        self._audio.terminate()


async def stream_microphone_transcripts() -> AsyncIterator[str]:
    api_key = os.environ["OPENAI_API_KEY"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "realtime=v1",
    }
    async with websockets.connect(OPENAI_REALTIME_URL, extra_headers=headers) as ws:
        await ws.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "turn_detection": {"type": "server_vad"},
                        "input_audio_format": "pcm16",
                        "input_audio_transcription": {"model": "whisper-1"},
                        "modalities": ["text"],
                    },
                }
            )
        )
        with MicrophoneStream() as mic:
            async def send_audio() -> None:
                for chunk in mic.generator():
                    await ws.send(
                        json.dumps(
                            {
                                "type": "input_audio_buffer.append",
                                "audio": base64.b64encode(chunk).decode("ascii"),
                            }
                        )
                    )
                await ws.send(json.dumps({"type": "input_audio_buffer.commit"}))

            sender = asyncio.create_task(send_audio())
            try:
                async for message in ws:
                    event = json.loads(message)
                    event_type = event.get("type", "")
                    if event_type in ("conversation.item.input_audio_transcription.delta", "response.audio_transcript.delta"):
                        delta = event.get("delta", "")
                        if delta:
                            yield delta
                    elif event_type in ("conversation.item.input_audio_transcription.completed", "response.audio_transcript.done"):
                        text = event.get("transcript", "") or event.get("text", "")
                        if text:
                            yield text
            finally:
                mic.close()
                sender.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await sender


async def main() -> None:
    async for transcript in stream_microphone_transcripts():
        print(transcript, flush=True)


if __name__ == "__main__":
    import contextlib

    asyncio.run(main())
