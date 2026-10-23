from typing import Dict, Any

# Local helpers for request/response normalization


def build_stream_request(
    audio_bytes: bytes,
    model: str = "nishat",
    language: str = "en-US",
    punctuate: bool = True,
) -> Dict[str, Any]:
    """Normalize audio and parameters into a Deepgram streaming request payload."""
    return {
        "model": model,
        "language": language,
        "punctuate": punctuate,
        "audio": audio_bytes,
    }


def normalize_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Extract useful fields from raw Deepgram streaming response."""
    return {
        "is_final": raw.get("final", False),
        "transcript": raw.get("transcript", ""),
    }
