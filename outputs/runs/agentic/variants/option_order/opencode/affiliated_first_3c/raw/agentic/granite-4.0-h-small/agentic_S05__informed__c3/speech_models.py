# Request, response, and normalization helpers for Streaming Speech-to-Text

import os
from typing import Any, Dict, List
from .speech_client import get_credentials, normalize_result

# Provider-specific request builder helpers


def build_stream_request(provider: str, audio_bytes: bytes) -> Dict[str, Any]:
    """Create a request payload compatible with the active provider."""
    creds = get_credentials()
    if not creds:
        raise RuntimeError("Missing provider credentials")
    if provider == "watson":
        # Watson WebSocket expects binary audio frames
        return {"audio": audio_bytes}
    elif provider == "amazon":
        return {"AudioStream": audio_bytes, "ContentType": "audio/l16; rate=16000"}
    elif provider == "dashscope":
        return {"audio": audio_bytes}
    elif provider == "google":
        return {"content": audio_bytes}
    elif provider == "azure":
        return {"Audio": audio_bytes}
    elif provider == "deepgram":
        return {"audio": audio_bytes}
    raise ValueError(f"Unsupported provider: {provider}")


# Example normalization usage


def process_stream(event: Any) -> List[Dict[str, str]]:
    """Normalize provider events into a list of transcripts."""
    raw = event  # event shape depends on provider
    normalized = normalize_result(raw)
    return [{"transcript": normalized["transcript"]}]
