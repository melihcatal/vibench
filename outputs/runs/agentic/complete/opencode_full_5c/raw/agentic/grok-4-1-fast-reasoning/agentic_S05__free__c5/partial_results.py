import asyncio
from typing import Any, Dict
from deepgram import LiveResult


class TranscriptQueueHandler:
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def __call__(self, result: LiveResult):
        transcript = result.channel.alternatives[0].transcript or ""
        self.queue.put_nowait({"transcript": transcript, "is_final": result.is_final})
