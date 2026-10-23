import asyncio
from typing import Dict, Any

# Provider-agnostic helpers for handling streaming transcription events


class PartialResult:
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.transcript = raw.get("transcript", "")
        self.is_final = raw.get("final", False)

    @classmethod
    async def from_event(cls, event):
        # Assume 'event' is an async iterator item representing a recognition result
        return cls(event)


async def handle_partial_results(events):
    """Yield PartialResult objects as streaming events arrive."""
    async for event in events:
        yield await PartialResult.from_event(event)

    # Placeholder for real event source (e.g., Deepgram SDK result stream)
    # async for chunk in stream.results():
    #     yield await PartialResult.from_event(chunk)
