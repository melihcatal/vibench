from typing import AsyncIterator
from speech_models import TranscriptEvent

async def handle_partial_results(stream) -> AsyncIterator[str]:
    async for event in stream:
        if isinstance(event, dict):
            transcript_event = TranscriptEvent(**event)
        else:
            transcript_event = event

        if transcript_event.is_final:
            yield transcript_event.text
        else:
            yield f"[Interim: {transcript_event.text}]"