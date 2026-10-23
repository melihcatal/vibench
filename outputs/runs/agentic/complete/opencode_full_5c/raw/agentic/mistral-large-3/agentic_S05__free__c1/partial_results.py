from typing import Dict, Any


class PartialResultHandler:
    """Handles partial and final streaming recognition events."""

    def __init__(self):
        self._current_transcript = ""
        self._final_transcripts = []

    def handle_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Processes a streaming recognition result."""
        if result["is_final"]:
            self._final_transcripts.append(result["transcript"])
            self._current_transcript = ""
            return {
                "type": "final",
                "transcript": result["transcript"],
                "all_final_transcripts": self._final_transcripts.copy(),
            }
        else:
            self._current_transcript = result["transcript"]
            return {
                "type": "partial",
                "transcript": self._current_transcript,
                "stability": result["stability"],
            }

    def get_final_transcripts(self) -> list:
        """Returns all final transcripts."""
        return self._final_transcripts.copy()
