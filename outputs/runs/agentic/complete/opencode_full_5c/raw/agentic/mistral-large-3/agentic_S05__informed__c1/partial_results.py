from typing import Dict, Any, Optional


def handle_partial_result(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Handles partial and final streaming recognition events from IBM Watson STT.
    Normalizes the event into a consistent format.
    """
    if event.get("results"):
        result = event["results"][0]
        if result.get("final"):
            return {
                "type": "final",
                "text": result["alternatives"][0]["transcript"],
                "confidence": result["alternatives"][0].get("confidence", 0.0),
            }
        else:
            return {"type": "interim", "text": result["alternatives"][0]["transcript"]}
    return None


def normalize_transcript(event: Dict[str, Any]) -> Optional[str]:
    """
    Extracts and normalizes transcript text from IBM Watson STT events.
    """
    if event.get("results"):
        result = event["results"][0]
        return result["alternatives"][0]["transcript"]
    return None
