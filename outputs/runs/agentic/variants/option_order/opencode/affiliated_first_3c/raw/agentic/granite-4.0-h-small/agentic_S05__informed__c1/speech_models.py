"""
Request, response, and normalization helpers for Streaming Speech-to-Text.
Provider: IBM Watson Speech-to-Text WebSocket.
"""

import json
from typing import Dict, Any, Optional


def build_handshake_request(
    language: str = "en-US", punctuation: bool = True
) -> Dict[str, Any]:
    """
    Constructs the initial handshake payload for Watson STT WebSocket.
    Args:
        language: BCP-47 language code (default 'en-US').
        punctuation: Enable automatic punctuation.
    Returns: Dict with session initialization fields.
    """
    return {
        "action": "start",
        "model": f"en-US_BroadbandModel",  # placeholder model
        "language": language,
        "continuous": True,
        "interim_results": True,
        "max_alternatives": 3,
        "punctuation": punctuation,
    }


def parse_watson_response(raw: str) -> Optional[Dict[str, Any]]:
    """
    Parses a raw JSON string from Watson streaming response.
    Returns parsed dict or None if malformed.
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def normalize_alternative(alternative: Dict[str, Any]) -> str:
    """
    Returns the clean transcript from a Watson alternative dict.
    Removes extra spaces before punctuation.
    """
    try:
        transcript = alternative["transcript"]
        # Watson may add space before punctuation
        transcript = transcript.replace(" .", ".").replace(" ,", ",").replace(" ;", ";")
        return transcript.strip()
    except (KeyError, TypeError):
        return ""


def extract_final(response: Dict[str, Any]) -> str:
    """
    Extracts the final recognized transcript from a complete Watson response.
    Looks for the last result's first alternative.
    """
    try:
        final_result = response["results"][-1]
        alt = final_result["alternatives"][0]
        return normalize_alternative(alt)
    except (KeyError, IndexError, TypeError):
        return ""


if __name__ == "__main__":
    # Example usage (replace with real response JSON)
    sample = json.dumps(
        {"results": [{"alternatives": [{"transcript": "hello world"}]}]}
    )
    parsed = parse_watson_response(sample)
    if parsed:
        final_text = extract_final(parsed)
        print("Final recognized text:", final_text)
