"""
Handle partial and final streaming recognition events from Google Cloud Speech-to-Text.

Processes streaming recognition responses, distinguishes between interim (partial)
and final results, and provides callback-based event handling for real-time transcription.

Provider: Google Cloud Speech-to-Text
SDK: google-cloud-speech
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from google.cloud.speech_v1p1beta1 import types as speech_types

from speech_models import (
    StreamingTranscriptSegment,
    StreamingTranscriptResult,
    normalize_streaming_response,
)


class ResultType(Enum):
    """Type of streaming recognition result."""

    INTERIM = "interim"
    FINAL = "final"
    ERROR = "error"


@dataclass
class RecognitionEvent:
    """Represents a single recognition event from streaming speech."""

    event_type: ResultType
    text: str
    confidence: float
    timestamp: float = field(default_factory=time.time)
    is_final: bool = False
    result_index: int = 0
    stability: float = 0.0
    language_code: str = ""
    raw_result: Optional[dict] = field(default=None, repr=False)


class StreamingResultHandler:
    """
    Handles partial and final streaming recognition events from Google Cloud Speech-to-Text.

    Provides callback registration, event processing, and aggregation of streaming
    transcription results into a coherent transcript.
    """

    def __init__(
        self,
        on_interim: Optional[Callable[[RecognitionEvent], None]] = None,
        on_final: Optional[Callable[[RecognitionEvent], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialize the streaming result handler.

        Args:
            on_interim: Callback for interim (partial) results.
            on_final: Callback for final results.
            on_error: Callback for errors.
            on_complete: Callback with full aggregated transcript on completion.
        """
        self._on_interim = on_interim
        self._on_final = on_final
        self._on_error = on_error
        self._on_complete = on_complete
        self._all_final_segments: list[str] = []
        self._event_count = 0
        self._current_interim: Optional[str] = None

    def process_response(
        self, response: speech_types.StreamingRecognizeResponse
    ) -> list[RecognitionEvent]:
        """
        Process a single Google Cloud Speech streaming response and fire callbacks.

        Args:
            response: Raw StreamingRecognizeResponse from the API.

        Returns:
            List of RecognitionEvent objects generated from this response.
        """
        events: list[RecognitionEvent] = []
        normalized_results = normalize_streaming_response(response)

        for result in normalized_results:
            for segment in result.segments:
                event = RecognitionEvent(
                    event_type=ResultType.FINAL if result.is_final else ResultType.INTERIM,
                    text=segment.text,
                    confidence=segment.confidence,
                    is_final=result.is_final,
                    result_index=result.result_id,
                    stability=result.stability,
                    language_code=segment.language_code,
                    raw_result={
                        "result_index": result.result_id,
                        "is_final": result.is_final,
                        "stability": result.stability,
                    },
                )

                events.append(event)
                self._event_count += 1

                if result.is_final:
                    self._all_final_segments.append(segment.text)
                    if self._on_final:
                        self._on_final(event)
                else:
                    self._current_interim = segment.text
                    if self._on_interim:
                        self._on_interim(event)

        return events

    def process_error(self, error: Exception) -> RecognitionEvent:
        """
        Process an error event and fire the error callback.

        Args:
            error: The exception that occurred.

        Returns:
            RecognitionEvent representing the error.
        """
        event = RecognitionEvent(
            event_type=ResultType.ERROR,
            text="",
            confidence=0.0,
            is_final=True,
        )

        if self._on_error:
            self._on_error(error)

        return event

    def finalize(self) -> str:
        """
        Finalize processing and return the aggregated transcript.

        Fires the on_complete callback with the full transcript.

        Returns:
            Complete aggregated final transcript text.
        """
        full_text = " ".join(self._all_final_segments).strip()

        if self._on_complete:
            self._on_complete(full_text)

        return full_text

    @property
    def current_interim(self) -> Optional[str]:
        """Get the most recent interim text."""
        return self._current_interim

    @property
    def final_transcript(self) -> str:
        """Get the aggregated final transcript so far."""
        return " ".join(self._all_final_segments).strip()

    @property
    def event_count(self) -> int:
        """Get the total number of events processed."""
        return self._event_count


async def async_stream_event_handler(
    response_iterator: Any,
    handler: StreamingResultHandler,
) -> AsyncGenerator[RecognitionEvent, None]:
    """
    Async wrapper that processes a Google Cloud Speech response iterator
    through a StreamingResultHandler and yields RecognitionEvents.

    Args:
        response_iterator: Iterator of StreamingRecognizeResponse from the API.
        handler: StreamingResultHandler instance with registered callbacks.

    Yields:
        RecognitionEvent objects as they are processed.
    """
    for response in response_iterator:
        try:
            events = handler.process_response(response)
            for event in events:
                yield event
        except Exception as e:
            error_event = handler.process_error(e)
            yield error_event
            break

    final_text = handler.finalize()
    yield RecognitionEvent(
        event_type=ResultType.FINAL,
        text=final_text,
        confidence=1.0,
        is_final=True,
    )
