# [HELPER] speech_models.py

from typing import Dict, Any

# Identify provider: Google Cloud Speech-to-Text


def normalize_response(response: Any) -> Dict:
    """Convert protobuf response to plain dict."""
    result = {}
    for event in response.results:
        for alt in event.alternatives:
            result["transcript"] = alt.transcript
            result["is_final"] = event.is_final
            result["confidence"] = alt.confidence
    return result
