from typing import Dict, Any


class PartialResultHandler:
    def __init__(self):
        self._final_transcript = []
        self._current_speaker = None

    def handle(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if result["is_final"]:
            self._final_transcript.append(result["transcript"])
            return {
                "type": "final",
                "transcript": result["transcript"],
                "confidence": result["confidence"],
                "full_transcript": " ".join(self._final_transcript),
            }
        else:
            return {
                "type": "interim",
                "transcript": result["transcript"],
                "confidence": result.get("confidence", 0.0),
            }

    def get_full_transcript(self) -> str:
        return " ".join(self._final_transcript)
