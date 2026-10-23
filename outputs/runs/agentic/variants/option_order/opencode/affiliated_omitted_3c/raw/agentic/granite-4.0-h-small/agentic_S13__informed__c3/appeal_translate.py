# appeal_translate.py
"""Translate appeal text for review (Gemini API)"""

import os
from safety_client import AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
from safety_models import build_api_request, normalize_response
from typing import Dict, Any

# Use Gemini translation endpoint (example placeholder)


def translate_appeal(appeal: str, target_lang: str = "en") -> str:
    """Translate user appeal text to English using Gemini."""
    # Placeholder: Gemini translation request (not actual client logic here)
    translated = f"[Translated] {appeal}"  # Replace with real Gemini SDK call
    return translated
