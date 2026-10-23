# [HELPER] speech_models.py
# Define local request, response, and normalization helpers for Text-to-Speech

from __future__ import annotations
from typing import TypedDict, Optional, List
from dataclasses import dataclass

# ----- Request models -------------------------------------------------------


class SynthesisRequest(TypedDict):
    """Base request for synthesizing text.

    Attributes:
        text (str): Plain text.
        ssml (str, optional): SSML string (if provided, text is ignored).
        voice_name (str, optional): Voice identifier.
        locale (str, optional): Locale for voice selection.
    """

    text: str
    ssml: Optional[str] = None
    voice_name: Optional[str] = None
    locale: str = "en-US"


# ----- Response models -------------------------------------------------------


class SynthesisResponse(TypedDict):
    """Response envelope for synthesized audio.

    Attributes:
        audio_bytes (bytes): Raw PCM/WAV audio data.
        duration_ms (int, optional): Audio length in milliseconds.
        format (str, optional): Audio format identifier.
    """

    audio_bytes: bytes
    duration_ms: Optional[int] = None
    format: str = "wav"


# ----- Normalization utilities ----------------------------------------------


def normalize_locale(locale: str) -> str:
    """Convert user input to a standard BCP‑47 code.

    Args:
        locale (str): Arbitrary locale string (e.g., 'en_US').

    Returns:
        str: Normalized locale like 'en-US'.
    """
    parts = locale.split("_")
    if len(parts) == 2:
        return f"{parts[0]}-{parts[1].upper()}"
    return locale


# Example helper to build an SSML request from plain text


def build_ssml(
    text: str, voice_name: str = "en-US-JennyNeural", rate: str = "medium"
) -> str:
    """Create a simple SSML wrapper with prosody controls.

    Args:
        text (str): Plain text to read.
        voice_name (str): Voice identifier.
        rate (str): Prosody rate (fast/medium/slow).

    Returns:
        str: SSML string ready for synthesis.
    """
    rate_factor = {"slow": "0.75", "medium": "1.0", "fast": "1.25"}.get(rate, "1.0")
    return (
        f"<speak version='1.0' xml:lang='{normalize_locale('en-US')}'>"
        f"<voice name='{voice_name}'><prosody rate='{rate_factor}'>{text}</prosody></voice></speak>"
    )


# ----- Usage examples (for local testing only) ------------------------------
if __name__ == "__main__":
    example = build_ssml("Hello, world!", voice_name="en-US-JennyNeural", rate="fast")
    print("Generated SSML:", example)
