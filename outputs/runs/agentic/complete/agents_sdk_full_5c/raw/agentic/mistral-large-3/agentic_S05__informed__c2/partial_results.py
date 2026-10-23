from typing import AsyncIterable
from speech_models import TranscriptEvent

class PartialResultHandler:
    def __init__(self):
        self.buffer = ""

    async def handle_events(self, events: AsyncIterable[TranscriptEvent]):
        async for event in events:
            if event.is_final:
                self.buffer = ""
                yield event.transcript, True
            else:
                self.buffer = event.transcript
                yield self.buffer, False