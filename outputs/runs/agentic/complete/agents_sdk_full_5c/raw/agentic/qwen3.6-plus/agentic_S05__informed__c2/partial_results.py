"""
Handles partial and final streaming recognition events from Google Cloud Speech-to-Text.
Provides event handlers, callbacks, and result aggregation for streaming transcription.

Provider: Google Cloud Speech-to-Text Streaming API
SDK: google-cloud-speech
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import logging
from collections.abc import Callable
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech

from speech_models import (
    FinalTranscriptResult,
    PartialTranscriptResult,
    extract_final_results,
    normalize_streaming_response,
)

logger = logging.getLogger(__name__)


def handle_streaming_response(
    response: speech.StreamingRecognizeResponse,
) -> list[PartialTranscriptResult]:
    """
    Handle a Google Cloud streaming recognition response and extract partial results.

    Args:
        response: StreamingRecognizeResponse from Google Cloud Speech API.

    Returns:
        List of PartialTranscriptResult objects.
    """
    partial_results = normalize_streaming_response(response)
    for result in partial_results:
        if result.is_final:
            logger.debug(f"Final transcript: {result.transcript} (confidence: {result.confidence:.2f})")
        else:
            logger.debug(f"Interim transcript: {result.transcript}")
    return partial_results


class StreamingTranscriptHandler:
    """
    Manages partial and final streaming recognition events.

    Provides callbacks for interim and final results, and maintains
    an aggregated transcript buffer.
    """

    def __init__(
        self,
        on_interim: Optional[Callable[[PartialTranscriptResult], None]] = None,
        on_final: Optional[Callable[[FinalTranscriptResult], None]] = None,
    ):
        """
        Initialize the streaming transcript handler.

        Args:
            on_interim: Callback for interim transcript results.
            on_final: Callback for final transcript results.
        """
        self.on_interim = on_interim
        self.on_final = on_final
        self._final_results: list[FinalTranscriptResult] = []
        self._current_interim: Optional[PartialTranscriptResult] = None

    def process_response(self, response: speech.StreamingRecognizeResponse) -> list[PartialTranscriptResult]:
        """
        Process a Google Cloud streaming response and dispatch callbacks.

        Args:
            response: StreamingRecognizeResponse from Google Cloud Speech API.

        Returns:
            List of PartialTranscriptResult objects.
        """
        partial_results = handle_streaming_response(response)

        for partial in partial_results:
            if partial.is_final:
                final = extract_final_results([partial])
                if final:
                    self._final_results.extend(final)
                    if self.on_final:
                        self.on_final(final[0])
            else:
                self._current_interim = partial
                if self.on_interim:
                    self.on_interim(partial)

        return partial_results

    def get_aggregated_transcript(self) -> str:
        """
        Get the full aggregated transcript from all final results.

        Returns:
            Concatenated transcript text.
        """
        parts = [r.transcript for r in self._final_results if r.transcript]
        return " ".join(parts).strip()

    def get_final_results(self) -> list[FinalTranscriptResult]:
        """Return all finalized results collected so far."""
        return list(self._final_results)

    @property
    def current_interim(self) -> Optional[PartialTranscriptResult]:
        """Return the current interim result, if any."""
        return self._current_interim


def filter_low_confidence_results(
    results: list[PartialTranscriptResult],
    min_confidence: float = 0.5,
) -> list[PartialTranscriptResult]:
    """
    Filter out results below a confidence threshold.

    Args:
        results: List of PartialTranscriptResult objects.
        min_confidence: Minimum confidence threshold (0.0 to 1.0).

    Returns:
        Filtered list of results meeting the confidence threshold.
    """
    return [r for r in results if r.confidence >= min_confidence]


def merge_overlapping_results(
    results: list[PartialTranscriptResult],
) -> list[PartialTranscriptResult]:
    """
    Merge overlapping interim results, keeping the most recent for each segment.

    Google Cloud Speech may return overlapping interim results; this keeps
    only the latest version for each result ID.

    Args:
        results: List of PartialTranscriptResult objects.

    Returns:
        Deduplicated list of results.
    """
    seen_transcripts: dict[str, PartialTranscriptResult] = {}
    for result in results:
        if result.transcript and (
            result.transcript not in seen_transcripts
            or result.is_final
        ):
            seen_transcripts[result.transcript] = result
    return list(seen_transcripts.values())
