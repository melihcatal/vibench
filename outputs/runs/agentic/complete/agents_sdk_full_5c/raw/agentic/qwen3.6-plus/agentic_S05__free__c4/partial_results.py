"""Handles partial and final streaming recognition events from Google Cloud Speech-to-Text."""

from typing import Callable, Dict, List, Optional

from google.cloud import speech_v1p1beta1 as speech

from speech_client import create_streaming_recognition_config, get_speech_client
from speech_models import (
    StreamingSpeechEvent,
    TranscriptSegment,
    normalize_streaming_result,
)


class PartialResultHandler:
    """Manages partial (interim) and final transcript events from Google Cloud Speech streaming.

    Tracks interim results, promotes them to final when is_final=True,
    and invokes registered callbacks for each event type.
    """

    def __init__(
        self,
        language_code: str = "en-US",
        sample_rate_hertz: int = 16000,
        model: str = "latest_long",
    ):
        self.language_code = language_code
        self.model = model
        self._interim_buffer: Dict[int, TranscriptSegment] = {}
        self._final_segments: List[TranscriptSegment] = []
        self._on_interim: Optional[Callable[[TranscriptSegment], None]] = None
        self._on_final: Optional[Callable[[TranscriptSegment], None]] = None
        self._on_error: Optional[Callable[[str], None]] = None

    def on_interim(self, callback: Callable[[TranscriptSegment], None]):
        """Register a callback invoked when a partial/interim result arrives from Google Cloud Speech."""
        self._on_interim = callback

    def on_final(self, callback: Callable[[TranscriptSegment], None]):
        """Register a callback invoked when a final result arrives from Google Cloud Speech."""
        self._on_final = callback

    def on_error(self, callback: Callable[[str], None]):
        """Register a callback for streaming errors."""
        self._on_error = callback

    def process_response(self, response: speech.StreamingRecognizeResponse) -> StreamingSpeechEvent:
        """Process a single Google Cloud StreamingRecognizeResponse and dispatch events.

        Routes interim results (is_final=False) and final results (is_final=True)
        through the registered callbacks and normalizes them into StreamingSpeechEvent objects.
        """
        event = StreamingSpeechEvent()

        for result in response.results:
            segment = normalize_streaming_result(result)

            if result.is_final:
                self._final_segments.append(segment)
                if self._on_final:
                    self._on_final(segment)
            else:
                stability_key = result.stability
                self._interim_buffer[stability_key] = segment
                if self._on_interim:
                    self._on_interim(segment)

            event.segments.append(segment)

        return event

    def process_stream(
        self,
        responses: List[speech.StreamingRecognizeResponse],
    ) -> List[StreamingSpeechEvent]:
        """Process a batch of Google Cloud streaming responses and return events."""
        events = []
        for response in responses:
            event = self.process_response(response)
            events.append(event)
        return events

    def get_final_transcript(self) -> str:
        """Return the concatenated final transcript text from Google Cloud Speech results."""
        return " ".join(s.text for s in self._final_segments if s.text.strip()).strip()

    def get_all_segments(self) -> List[TranscriptSegment]:
        """Return all segments (final + current interim) from the Google Cloud Speech session."""
        return self._final_segments + list(self._interim_buffer.values())

    def reset(self):
        """Clear all buffers and segment history for a new Google Cloud Speech streaming session."""
        self._interim_buffer.clear()
        self._final_segments.clear()


def handle_streaming_responses(
    responses,
    on_interim: Optional[Callable[[TranscriptSegment], None]] = None,
    on_final: Optional[Callable[[TranscriptSegment], None]] = None,
    on_error: Optional[Callable[[str], None]] = None,
    language_code: str = "en-US",
) -> List[StreamingSpeechEvent]:
    """Convenience function to process Google Cloud Speech streaming responses with callbacks.

    Uses google.cloud.speech_v1p1beta1 SDK for response handling.
    """
    handler = PartialResultHandler(language_code=language_code)
    handler.on_interim(on_interim or (lambda s: None))
    handler.on_final(on_final or (lambda s: None))
    handler.on_error(on_error or (lambda e: print(f"Error: {e}")))

    events = handler.process_stream(responses)
    return events
