from typing import Dict, Any


class PartialResultHandler:
    def __init__(self):
        self._final_transcript = []
        self._partial_transcript = ""

    def handle(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if result["is_final"]:
            self._final_transcript.append(result["transcript"])
            self._partial_transcript = ""
            return {
                "event": "final",
                "transcript": result["transcript"],
                "full_transcript": " ".join(self._final_transcript),
            }
        else:
            self._partial_transcript = result["transcript"]
            return {
                "event": "partial",
                "transcript": self._partial_transcript,
                "stability": result["stability"],
            }

    def get_full_transcript(self) -> str:
        return " ".join(self._final_transcript)
