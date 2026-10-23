from typing import AsyncGenerator, Dict, Any

from speech_models import SpeechEvent


class PartialResultHandler:
    """Handles partial and final streaming recognition events from DashScope."""

    def __init__(self):
        self.buffer = []

    async def handle_events(
        self, events: AsyncGenerator[SpeechEvent, None]
    ) -> AsyncGenerator[str, None]:
        """Process speech events and yield transcript segments."""
        async for event in events:
            if event.is_final:
                self.buffer.append(event.text)
                yield " ".join(self.buffer)
                self.buffer = []
            else:
                self.buffer.append(event.text)
                yield " ".join(self.buffer)
