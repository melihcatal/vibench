"""
Handle partial and final streaming recognition events from Google Cloud Speech-to-Text.

This module provides event-driven processing of streaming speech recognition
results from the Google Cloud Speech API (speech.googleapis.com). It distinguishes
between interim (partial) and final results, manages result aggregation, and
emits structured events for downstream consumers.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import AsyncIterator, Callable, Awaitable, List

logger = logging.getLogger(__name__)

GOOGLE_CLOUD_SPEECH_API_ENDPOINT = "speech.googleapis.com"


class ResultType(str, Enum):
    INTERIM = "interim"
    FINAL = "final"
    VOICE_ACTIVITY_START = "voice_activity_start"
    VOICE_ACTIVITY_END = "voice_activity_end"


@dataclass
class RecognitionEvent:
    """Structured event from a streaming recognition result."""
    event_type: ResultType
    text: str
    confidence: float = 0.0
    stability: float = 0.0
    is_final: bool = False
    alternatives: List[dict] = field(default_factory=list)
    result_index: int = 0
    timestamp_ms: float = 0.0


class PartialResultsHandler:
    """
    Process and manage partial/final streaming recognition events.

    Buffers interim results and promotes them to final when the Google Cloud
    Speech-to-Text API returns a final flag. Supports callbacks for different
    event types.
    """

    def __init__(
        self,
        on_final: Callable[[RecognitionEvent], Awaitable[None]] | None = None,
        on_interim: Callable[[RecognitionEvent], Awaitable[None]] | None = None,
        on_voice_activity: Callable[[RecognitionEvent], Awaitable[None]] | None = None,
    ):
        self._on_final = on_final
        self._on_interim = on_interim
        self._on_voice_activity = on_voice_activity
        self._buffer: list[RecognitionEvent] = []
        self._result_counter: int = 0
        self._final_transcripts: list[str] = []

    @property
    def final_transcripts(self) -> list[str]:
        """Return all accumulated final transcript strings."""
        return list(self._final_transcripts)

    @property
    def full_transcript(self) -> str:
        """Return the concatenated full transcript."""
        return " ".join(self._final_transcripts).strip()

    def process_streaming_response(
        self, response: dict
    ) -> list[RecognitionEvent]:
        """
        Process a raw streaming recognition result dict and produce events.

        Args:
            response: Dict with keys 'text', 'is_final', 'confidence', 'stability',
                      optionally 'alternatives'.

        Returns:
            List of RecognitionEvent objects.
        """
        events: list[RecognitionEvent] = []

        text = response.get("text", "").strip()
        is_final = response.get("is_final", False)
        confidence = response.get("confidence", 0.0)
        stability = response.get("stability", 0.0)
        alternatives = response.get("alternatives", [])

        self._result_counter += 1

        if is_final and text:
            event = RecognitionEvent(
                event_type=ResultType.FINAL,
                text=text,
                confidence=confidence,
                stability=stability,
                is_final=True,
                alternatives=alternatives,
                result_index=self._result_counter,
            )
            self._final_transcripts.append(text)
            self._buffer.clear()
            events.append(event)
            logger.info(
                "Final result #%d from %s: %s",
                self._result_counter,
                GOOGLE_CLOUD_SPEECH_API_ENDPOINT,
                text,
            )
        elif text:
            event = RecognitionEvent(
                event_type=ResultType.INTERIM,
                text=text,
                confidence=confidence,
                stability=stability,
                is_final=False,
                alternatives=alternatives,
                result_index=self._result_counter,
            )
            # Update the buffer: replace last interim or append new
            if self._buffer and self._buffer[-1].event_type == ResultType.INTERIM:
                self._buffer[-1] = event
            else:
                self._buffer.append(event)
            events.append(event)
            logger.debug("Interim result #%d: %s", self._result_counter, text)

        return events

    async def handle_event(self, event: RecognitionEvent) -> None:
        """Dispatch a RecognitionEvent to the appropriate callback."""
        if event.event_type == ResultType.FINAL and self._on_final:
            await self._on_final(event)
        elif event.event_type == ResultType.INTERIM and self._on_interim:
            await self._on_interim(event)
        elif event.event_type in (ResultType.VOICE_ACTIVITY_START, ResultType.VOICE_ACTIVITY_END):
            if self._on_voice_activity:
                await self._on_voice_activity(event)


async def stream_partial_results(
    response_stream: AsyncIterator[dict],
    handler: PartialResultsHandler,
) -> AsyncIterator[RecognitionEvent]:
    """
    Consume a stream of raw recognition result dicts and emit structured events.

    Args:
        response_stream: Async iterator of raw result dicts.
        handler: PartialResultsHandler instance for event processing.

    Yields:
        RecognitionEvent instances as they are processed.
    """
    async for raw_response in response_stream:
        events = handler.process_streaming_response(raw_response)
        for event in events:
            await handler.handle_event(event)
            yield event
