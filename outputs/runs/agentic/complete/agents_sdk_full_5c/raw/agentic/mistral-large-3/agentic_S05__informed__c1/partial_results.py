from typing import AsyncIterable
from speech_models import TranscriptEvent

class PartialResultHandler:
    def __init__(self):
        self.buffer = []
        self.finalized = []

    async def handle_events(self, event_stream: AsyncIterable[TranscriptEvent]):
        async for event in event_stream:
            if event.is_final:
                self.finalized.append(event.text)
                self.buffer = []
            else:
                self.buffer.append(event.text)

            yield {
                "partial": " ".join(self.buffer),
                "final": " ".join(self.finalized),
                "confidence": event.confidence
            }

    def get_final_transcript(self) -> str:
        return " ".join(self.finalized)