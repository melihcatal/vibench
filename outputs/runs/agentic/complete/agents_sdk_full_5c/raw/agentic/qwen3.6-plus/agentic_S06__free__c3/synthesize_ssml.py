"""
synthesize_ssml.py - Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.

Uses the google-cloud-texttospeech SDK to convert SSML markup into audio.
Supports Google Cloud voice names, prosody controls (rate, pitch, volume),
breaks, emphasis, and other SSML elements.
"""

from __future__ import annotations

import os
import re
from typing import Optional

from speech_client import SpeechClientHelper
from speech_models import AudioEncodingEnum, SSMLGenderEnum, SSMLSynthesisRequest, SynthesisResponse


def wrap_ssml_in_speak(ssml: str) -> str:
    """Wrap raw SSML content in <speak> tags if not already present."""
    stripped = ssml.strip()
    if not stripped.startswith("<speak"):
        stripped = f"<speak>{stripped}</speak>"
    return stripped


def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: Optional[str] = None,
    ssml_gender: Optional[str] = None,
    encoding: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    volume_gain_db: float = 0.0,
    sample_rate_hertz: int = 24000,
    credentials_path: Optional[str] = None,
) -> SynthesisResponse:
    """
    Synthesize SSML markup to audio using Google Cloud Text-to-Speech (gcloud tts).

    Provider: Google Cloud Text-to-Speech via google-cloud-texttospeech SDK.
    API endpoint: texttospeech.googleapis.com

    Args:
        ssml: SSML markup string. Will be auto-wrapped in <speak> if needed.
        language_code: BCP-47 language code, e.g. "en-US", "ja-JP".
        voice_name: Specific Google voice name, e.g. "en-US-Wavenet-D".
        ssml_gender: Preferred voice gender: MALE, FEMALE, or NEUTRAL.
        encoding: Audio encoding - MP3, LINEAR16, OGG_OPUS, or MULAW.
        speaking_rate: Speed multiplier (0.25 to 4.0).
        pitch: Pitch shift in semitones (-20.0 to 20.0).
        volume_gain_db: Volume gain in decibels (-96.0 to 16.0).
        sample_rate_hertz: Audio sample rate (8000 to 48000).
        credentials_path: Path to Google service account JSON file.

    Returns:
        SynthesisResponse with audio_content bytes and metadata.

    Raises:
        ValueError: If SSML is empty or exceeds length limits.
        google.api_core.exceptions.GoogleAPIError: On Google Cloud API failure.
    """
    if not ssml or not ssml.strip():
        raise ValueError("SSML must not be empty.")

    normalized_ssml = wrap_ssml_in_speak(ssml)
    if len(normalized_ssml) > 5000:
        raise ValueError("SSML exceeds 5000 character limit for Google Cloud TTS.")

    gender = SSMLGenderEnum(ssml_gender) if ssml_gender else None
    audio_enc = AudioEncodingEnum(encoding.upper())

    request = SSMLSynthesisRequest(
        ssml=normalized_ssml,
        language_code=language_code,
        voice_name=voice_name,
        ssml_gender=gender,
        encoding=audio_enc,
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
        sample_rate_hertz=sample_rate_hertz,
    )

    client = SpeechClientHelper(credentials_path=credentials_path)
    response = client.synthesize_ssml(request)

    return response


def build_ssml_with_prosody(
    text: str,
    rate: str = "medium",
    pitch: str = "medium",
    volume: str = "medium",
    emphasis: Optional[str] = None,
    break_ms: Optional[int] = None,
) -> str:
    """
    Build SSML string with prosody and optional emphasis/break controls
    for use with Google Cloud Text-to-Speech.

    Args:
        text: The text content to speak.
        rate: Speaking rate - x-slow, slow, medium, fast, x-fast.
        pitch: Pitch - x-low, low, medium, high, x-high.
        volume: Volume - silent, x-soft, soft, medium, loud, x-loud.
        emphasis: Optional emphasis level - strong, moderate, reduced, none.
        break_ms: Optional pause duration in milliseconds (50-5000).

    Returns:
        SSML string ready for synthesis.
    """
    content = text.strip()

    if emphasis:
        content = f'<emphasis level="{emphasis}">{content}</emphasis>'

    if break_ms:
        content += f'<break time="{break_ms}ms"/>'

    ssml = (
        f'<prosody rate="{rate}" pitch="{pitch}" volume="{volume}">'
        f"{content}"
        f"</prosody>"
    )

    return f"<speak>{ssml}</speak>"


if __name__ == "__main__":
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    ssml_content = build_ssml_with_prosody(
        text="Welcome to our presentation.",
        rate="medium",
        pitch="medium",
        volume="medium",
        break_ms=500,
    )
    result = synthesize_ssml(
        ssml=ssml_content,
        language_code="en-US",
        voice_name="en-US-Wavenet-D",
        credentials_path=creds,
    )
    print(f"Synthesized {result.audio_length_bytes} bytes of {result.encoding.value} audio")
