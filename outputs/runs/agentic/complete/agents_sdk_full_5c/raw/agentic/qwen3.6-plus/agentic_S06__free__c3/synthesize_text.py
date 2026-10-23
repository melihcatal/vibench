"""
synthesize_text.py - Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

Uses the google-cloud-texttospeech SDK to convert plain text input into
encoded audio bytes (MP3 by default). Accepts optional voice, encoding,
speaking rate, pitch, and volume parameters.
"""

from __future__ import annotations

import os
from typing import Optional

from speech_client import SpeechClientHelper
from speech_models import AudioEncodingEnum, SSMLGenderEnum, SynthesisRequest, SynthesisResponse


def synthesize_text(
    text: str,
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
    Synthesize plain text to audio using Google Cloud Text-to-Speech (gcloud tts).

    Provider: Google Cloud Text-to-Speech via google-cloud-texttospeech SDK.
    API endpoint: texttospeech.googleapis.com

    Args:
        text: Plain text to synthesize (1-5000 chars).
        language_code: BCP-47 language code, e.g. "en-US", "fr-FR".
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
        ValueError: If text is empty or exceeds length limits.
        google.api_core.exceptions.GoogleAPIError: On Google Cloud API failure.
    """
    if not text or not text.strip():
        raise ValueError("Text must not be empty.")
    if len(text) > 5000:
        raise ValueError("Text exceeds 5000 character limit for Google Cloud TTS.")

    gender = SSMLGenderEnum(ssml_gender) if ssml_gender else None
    audio_enc = AudioEncodingEnum(encoding.upper())

    request = SynthesisRequest(
        text=text.strip(),
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
    response = client.synthesize_text(request)

    return response


if __name__ == "__main__":
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    result = synthesize_text(
        text="Hello, this is a demonstration of Google Cloud Text-to-Speech synthesis.",
        language_code="en-US",
        voice_name="en-US-Wavenet-D",
        credentials_path=creds,
    )
    print(f"Synthesized {result.audio_length_bytes} bytes of {result.encoding.value} audio at {result.sample_rate_hertz} Hz")
