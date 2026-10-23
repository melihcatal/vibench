# reviewer_brief_audio.py
"""Generate spoken briefs for moderation reviewers (Azure Speech TTS)"""

import os
from safety_client import AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
from safety_models import build_api_request, normalize_response
from typing import Dict, Any

# Azure Speech TTS client (provider-specific import shown below)


def generate_brief_audio(text: str, voice: str = "en-US-JennyNeural") -> bytes:
    """Create an audio file (bytes) of the moderator brief using Azure TTS."""
    # Placeholder: actual Azure Speech SDK call would go here
    audio_bytes = text.encode("utf-8")  # Mock: return UTF-8 bytes
    return audio_bytes
