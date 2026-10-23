from typing import Any, Dict, List


def create_request(text: str, voice: str, prosody: Dict[str, Any]) -> Dict[str, Any]:
    """Create a Text-to-Speech request."""
    return {
        'text': text,
        'voice': voice,
        'prosody': prosody
    }


def parse_response(response: Dict[str, Any]) -> str:
    """Parse a Text-to-Speech response."""
    return response.get('audio_content', '')


def normalize_prosody(prosody: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize prosody parameters."""
    normalized = {}
    for key, value in prosody.items():
        if isinstance(value, (int, float)):
            normalized[key] = round(value, 2)
        else:
            normalized[key] = value
    return normalized
