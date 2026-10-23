from typing import NamedTuple, List, Dict

# ------------------------------------------------------------------
# Request models (what you send to TTS services)
# ------------------------------------------------------------------


class TextToSpeechRequest(NamedTuple):
    text: str
    voice_id: str = "default"
    ssml: bool = False
    custom_params: Dict = None


class SSMLToSpeechRequest(NamedTuple):
    ssml: str
    voice_id: str
    prosody: Dict = None  # e.g., pitch, rate, volume adjustments


# ------------------------------------------------------------------
# Response models (what you get back)
# ------------------------------------------------------------------


class SynthesisResponse(NamedTuple):
    audio_content: bytes  # raw audio bytes (could be wav/mp3/etc.)
    audio_format: str = "wav"  # inferred or supplied format
    duration_ms: int = None  # optional duration


# ------------------------------------------------------------------
# Normalization helpers used across implementations
# ------------------------------------------------------------------


def normalize_text(text: str) -> str:
    """Trim whitespace and ensure UTF‑8 encoding for safety."""
    return text.strip()


def validate_voice_id(voice_id: str) -> str:
    """Simple sanity check – ensure non‑empty string."""
    if not voice_id:
        raise ValueError("voice_id cannot be empty")
    return voice_id


def ensure_audio_format(format_str: str) -> str:
    """Standardize audio format string."""
    return format_str.lower()
