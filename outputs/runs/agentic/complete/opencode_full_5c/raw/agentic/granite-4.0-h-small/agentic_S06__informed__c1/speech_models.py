# speech_models.py
import os
from google.cloud import texttospeech


class SynthesisRequest:
    """Container for normalized synthesis parameters."""

    def __init__(
        self,
        text=None,
        ssml=None,
        voice=None,
        language_code="en-US",
        audio_encoding="MP3",
    ):
        self.text = text
        self.ssml = ssml
        self.voice = voice  # voice name like 'en-US-Wavenet-D'
        self.language_code = language_code
        self.audio_encoding = audio_encoding


class SynthesisResponse:
    """Container for normalized synthesis response data."""

    def __init__(self, audio_content):
        self.audio_content = audio_content


def normalize_request(req):
    """Convert user‑provided data to a validated SynthesisRequest."""
    # Ensure we have either plain text or SSML, not both
    if req.text and req.ssml:
        raise ValueError("Provide either plain text or SSML, not both")
    # Default voice if none supplied
    if not req.voice:
        req.voice = "en-US-Wavenet-D"
    return req


def extract_audio(response):
    """Utility to extract audio bytes from a raw client response."""
    return response.audio_content
