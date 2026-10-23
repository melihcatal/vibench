import json
from typing import Dict, Any


def handle_partial_result(result: Dict[str, Any]) -> None:
    """
    Process a partial streaming recognition result.
    Extracts the transcript and indicates if it's an interim result.
    """
    alternatives = result.get("alternatives", [])
    if not alternatives:
        return
    alt = alternatives[0]
    transcript = alt.get("transcript", "")
    is_final = result.get("is_final", False)
    flag = "final" if is_final else "interim"
    print(f"[PARTIAL] {transcript} ({flag})")


def handle_final_result(result: Dict[str, Any]) -> None:
    """
    Process a final streaming recognition result.
    Prints the final transcript along with confidence (if available).
    """
    alternatives = result.get("alternatives", [])
    if not alternatives:
        return
    alt = alternatives[0]
    transcript = alt.get("transcript", "")
    confidence = alt.get("confidence", None)
    print(f"[FINAL] {transcript} (confidence={confidence})")
