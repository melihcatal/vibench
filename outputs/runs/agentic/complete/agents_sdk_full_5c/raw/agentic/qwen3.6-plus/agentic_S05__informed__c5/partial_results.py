"""Handles partial and final streaming recognition events from Google Cloud Speech-to-Text."""

from typing import Callable, Optional
from google.cloud.speech_v2.types import cloud_speech
from speech_models import StreamingSpeechResult, normalize_recognition_result


class PartialResultHandler:
    """
    Manages partial (interim) and final recognition events from Google Cloud Speech-to-Text.

    Tracks stability of interim results and provides callbacks for partial and final events.
    Uses google-cloud-speech SDK SpeechRecognitionResult types.
    """

    def __init__(
        self,
        on_partial: Optional[Callable[[StreamingSpeechResult], None]] = None,
        on_final: Optional[Callable[[StreamingSpeechResult], None]] = None,
        stability_threshold: float = 0.85,
    ):
        self.on_partial = on_partial
        self.on_final = on_final
        self.stability_threshold = stability_threshold
        self.current_partial: Optional[StreamingSpeechResult] = None
        self.final_results: list[StreamingSpeechResult] = []
        self.partial_history: list[StreamingSpeechResult] = []

    def handle_response(self, response: cloud_speech.StreamingRecognizeResponse) -> None:
        """
        Process a StreamingRecognizeResponse from google-cloud-speech SDK
        and dispatch to appropriate handlers based on result type.
        """
        for result in response.results:
            normalized = normalize_recognition_result(result)
            if result.is_final:
                self._handle_final(normalized)
            else:
                self._handle_partial(normalized)

    def _handle_partial(self, result: StreamingSpeechResult) -> None:
        """Process an interim result from google-cloud-speech streaming recognition."""
        self.current_partial = result
        self.partial_history.append(result)
        if self.on_partial:
            self.on_partial(result)

    def _handle_final(self, result: StreamingSpeechResult) -> None:
        """Process a final result and clear partial state."""
        self.final_results.append(result)
        self.current_partial = None
        if self.on_final:
            self.on_final(result)

    def is_stable(self) -> bool:
        """Check if current partial result exceeds the stability threshold."""
        if self.current_partial is None:
            return False
        return self.current_partial.stability >= self.stability_threshold

    def get_aggregated_transcript(self) -> str:
        """Return aggregated transcript text from all final results."""
        return " ".join(r.transcript for r in self.final_results if r.transcript)

    def get_current_transcript(self) -> str:
        """Return current transcript text (final if available, else partial)."""
        if self.current_partial and self.current_partial.transcript:
            return self.current_partial.transcript
        return self.get_aggregated_transcript()

    def reset(self) -> None:
        """Clear all state."""
        self.current_partial = None
        self.final_results.clear()
        self.partial_history.clear()


def extract_partial_text(response: cloud_speech.StreamingRecognizeResponse) -> str:
    """Extract the latest partial transcript text from a Google Cloud Speech response."""
    for result in response.results:
        if not result.is_final and result.alternatives:
            return result.alternatives[0].transcript
    return ""


def extract_final_text(response: cloud_speech.StreamingRecognizeResponse) -> str:
    """Extract the latest final transcript text from a Google Cloud Speech response."""
    for result in response.results:
        if result.is_final and result.alternatives:
            return result.alternatives[0].transcript
    return ""
