"""
Handle partial and final streaming recognition events from Google Cloud Speech-to-Text.

Processes StreamingRecognizeResponse events from the google-cloud-speech API,
distinguishes between interim (partial) and final results, manages result
aggregation, and provides callbacks for downstream consumers.
"""

from typing import Callable, Optional

from google.cloud import speech

from speech_models import (
    InterimTranscript,
    FinalTranscript,
    parse_streaming_response,
    normalize_transcript_text,
)

# Google Cloud Speech-to-Text provider event types
EVENT_INTERIM = "interim"
EVENT_FINAL = "final"
EVENT_ERROR = "error"


class PartialResultsHandler:
    """
    Handles partial (interim) and final streaming recognition events.

    Processes google.cloud.speech.StreamingRecognizeResponse objects,
    separates interim vs final results, and dispatches to registered
    callbacks with normalized transcript data.
    """

    def __init__(
        self,
        on_interim: Optional[Callable[[InterimTranscript], None]] = None,
        on_final: Optional[Callable[[FinalTranscript], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        aggregate_finals: bool = False,
    ):
        self._on_interim = on_interim
        self._on_final = on_final
        self._on_error = on_error
        self._aggregate_finals = aggregate_finals
        self._final_transcripts: list[str] = []
        self._current_interim: Optional[InterimTranscript] = None
        self._result_count = 0
        self._final_count = 0

    @property
    def final_transcript_count(self) -> int:
        return self._final_count

    @property
    def accumulated_text(self) -> str:
        """Return all accumulated final transcript text."""
        return " ".join(self._final_transcripts).strip()

    def process_response(self, response: speech.StreamingRecognizeResponse) -> list[dict]:
        """
        Process a Google Cloud StreamingRecognizeResponse and dispatch events.

        Parses the raw response from google.cloud.speech.SpeechClient,
        separates interim and final results, updates internal state,
        and invokes registered callbacks.

        Args:
            response: Raw StreamingRecognizeResponse from Google Cloud.

        Returns:
            List of event dicts with type, text, confidence, and raw transcript.
        """
        events = []

        try:
            transcripts = parse_streaming_response(response)
        except Exception as e:
            if self._on_error:
                self._on_error(e)
            events.append({"type": EVENT_ERROR, "error": str(e)})
            return events

        for transcript in transcripts:
            text = normalize_transcript_text(transcript.text)

            if isinstance(transcript, FinalTranscript):
                event = self._handle_final(transcript, text)
            else:
                event = self._handle_interim(transcript, text)

            if event:
                events.append(event)

        return events

    def _handle_interim(
        self, transcript: InterimTranscript, text: str
    ) -> Optional[dict]:
        """Handle an interim (partial) recognition result."""
        self._current_interim = transcript

        event = {
            "type": EVENT_INTERIM,
            "text": text,
            "confidence": transcript.confidence,
            "stability": transcript.stability,
            "raw": transcript,
        }

        if self._on_interim:
            self._on_interim(transcript)

        return event

    def _handle_final(
        self, transcript: FinalTranscript, text: str
    ) -> Optional[dict]:
        """Handle a final recognition result."""
        self._final_count += 1
        self._result_count += 1

        if self._aggregate_finals and text:
            self._final_transcripts.append(text)

        event = {
            "type": EVENT_FINAL,
            "text": text,
            "confidence": transcript.confidence,
            "language_code": transcript.language_code,
            "result_end_time_seconds": transcript.result_end_time_seconds,
            "raw": transcript,
        }

        if self._on_final:
            self._on_final(transcript)

        return event

    def reset(self):
        """Reset internal state for a new streaming session."""
        self._final_transcripts.clear()
        self._current_interim = None
        self._result_count = 0
        self._final_count = 0


def create_default_handler(
    show_interim: bool = True,
    show_final: bool = True,
) -> PartialResultsHandler:
    """
    Create a PartialResultsHandler with default print callbacks.

    Returns a handler configured to print interim and final results
    from Google Cloud Speech-to-Text streaming recognition.
    """

    def _on_interim(t: InterimTranscript):
        if show_interim:
            print(f"[INTERIM] (conf={t.confidence:.2f}, stability={t.stability:.2f}) {t.text}")

    def _on_final(t: FinalTranscript):
        if show_final:
            print(f"[FINAL]  (conf={t.confidence:.2f}) {t.text}")

    return PartialResultsHandler(
        on_interim=_on_interim,
        on_final=_on_final,
        aggregate_finals=True,
    )
