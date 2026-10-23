from typing import Dict, Any


class PartialResultHandler:
    """Handles partial and final streaming recognition events."""

    def __init__(self):
        self._last_transcript = ""
        self._final_transcripts = []

    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Processes a streaming recognition event."""
        transcript = event["transcript"]
        is_final = event["is_final"]
        stability = event.get("stability", 0.0)

        if is_final:
            self._final_transcripts.append(transcript)
            self._last_transcript = ""
            return {
                "type": "final",
                "transcript": transcript,
                "stability": stability,
                "all_final": " ".join(self._final_transcripts),
            }
        else:
            self._last_transcript = transcript
            return {
                "type": "partial",
                "transcript": transcript,
                "stability": stability,
            }

    def get_final_transcripts(self) -> str:
        """Returns all final transcripts as a single string."""
        return " ".join(self._final_transcripts)
