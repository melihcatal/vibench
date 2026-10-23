import json
from typing import Dict


def generate_audio_brief(retrieved: List[Dict[str, Any]]) -> Dict[str, str]:
    """Create a spoken brief from retrieved search results.

    Args:
        retrieved (List[Dict[str, Any]]): List of documents returned by search.

    Returns:
        Dict[str, str]: Audio brief content and metadata.
    """
    # Placeholder: synthesize speech with a TTS provider later
    brief_text = "\n".join(
        [doc.get("title", "") for doc in retrieved if "title" in doc]
    )
    return {
        "brief": brief_text,
        "format": "text",  # to be passed to TTS service
        "provider": "dummy_tts",  # replace with actual TTS provider
    }
