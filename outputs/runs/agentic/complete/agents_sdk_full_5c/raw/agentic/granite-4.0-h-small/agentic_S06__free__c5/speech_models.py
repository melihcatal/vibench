# speech_models.py
# [HELPER] Define local request, response, and normalization helpers for Google Cloud Text-to-Speech.

from typing import Dict, Any

def normalize_synthesis_input(text: str, ssml: bool = False) -> Dict[str, Any]:
    """Normalize plain text or SSML into the expected SynthesisInput format.

    Args:
        text: The raw input string.
        ssml: Flag indicating whether the input is SSML.

    Returns:
        Dict representing the SynthesisInput to be used in API calls.
    """
    return {'text': text} if not ssml else {'ssml': text}


def parse_audio_response(response_bytes: bytes) -> Dict[str, Any]:
    """Placeholder for parsing audio binary response.

    The TTS client returns binary audio; this stub shows where a parser could be added
    if the service returned structured metadata alongside raw audio (e.g., from a custom
    wrapper service). Currently returns empty dict as no parsing is needed.
    """
    return {}
