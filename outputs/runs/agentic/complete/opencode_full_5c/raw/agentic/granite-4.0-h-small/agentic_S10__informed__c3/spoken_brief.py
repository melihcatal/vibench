import os
import json
from typing import Optional

import elevenlabs

from model_client import CLIENT_MAP, validate_provider
from model_models import (
    build_extract_json_request,
    normalize_extract_json_output,
)

# ---------------------------------------------------------------------------
# Configuration\n# ---------------------------------------------------------------------------
DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "elevenlabs")
validate_provider(DEFAULT_PROVIDER)

# ---------------------------------------------------------------------------
# Public API\n# ---------------------------------------------------------------------------

def generate_spoken_brief(
    text: str,
    provider: Optional[str] = None,
    speed: float = 1.0,
    temperature: float = 0.0,
) -> bytes:
    """
    Convert a text excerpt into a short spoken audio brief using a TTS provider.
    
    Args:
        text: content to be spoken.
        provider: optional hosted model; defaults to env DEFAULT_PROVIDER.
        speed: playback speed multiplier.
        temperature: sampling temperature for voice variability.
    
    Returns:
        Bytes representing an MP3 (or provider‑specific) audio file.
    """
    provider = provider or DEFAULT_PROVIDER
    provider = provider.lower()
    if provider != "elevenlabs":
        raise NotImplementedError(f"Spoken brief only implemented for ElevenLabs (provider={provider})")
    payload = build_extract_json_request(
        text,
        schema={"audio": ""},
        model_provider=provider,
        temperature=temperature,
    )
    payload["messages"] = [
        {"role": "user", "content": f"Speak the following in a crisp brief, speed {speed}x:\n\n{text}"}
    ]
    raw = _call_provider(provider, payload)
    return normalize_extract_json_output(raw) or b""


def _call_provider(payload: Dict[str, Any]) -> Any:
    # ElevenLabs expects a POST to its /voices/{voice_id}/tts endpoint.
    # We use the SDK for simplicity: elevenlabs.get_voice_clones returns a voice object; then voice.tts(text, ...).
    # Validate we have a voice clone ID configured via env variable.
    VOICE_CLONE_ID = os.getenv("ELEVEN_CLONE_ID")
    if not VOICE_CLONE_ID:
        raise RuntimeError("Set ELEVEN_CLONE_ID environment variable to an ElevenLabs voice clone ID.")
    voice = elevenlabs.Voice(VOICE_CLONE_ID)
    # SDK call returns raw bytes (MP3)
    return voice.tts(text=payload["messages"][0]["content"], speed=speed, temperature=temperature)

# ---------------------------------------------------------------------------
# CLI helper (optional)\n# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(os.sys.argv) < 2:
        print("Usage: python spoken_brief.py <text> [--speed <float>] [--temperature <float>]\")
        os.sys.exit(1)
    text = os.sys.argv[1]
    speed = temperature = None
    i = 2
    while i < len(os.sys.argv):
        if os.sys.argv[i] == "--speed":
            speed = float(os.sys.argv[i + 1])
            i += 2
        elif os.sys.argv[i] == "--temperature":
            temperature = float(os.sys.argv[i + 1])
            i += 2
        else:
            i += 1
    audio_bytes = generate_spoken_brief(text, speed=speed, temperature=temperature)
    # Write to a temporary file for listening (optional)
    import tempfile, base64
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(audio_bytes)
        print(f"Wrote audio to {tmp.name}")
