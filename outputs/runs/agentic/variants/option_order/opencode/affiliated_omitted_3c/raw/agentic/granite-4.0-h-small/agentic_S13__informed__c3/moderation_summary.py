# moderation_summary.py
"""Summarize moderation decisions (Mistral Chat API)"""

import os
from safety_client import AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
from safety_models import build_api_request, normalize_response
from typing import Dict, Any

# For summary we can reuse Azure moderation results or combine with LLM


def summarize_moderation(text: str, unsafe_spans: List[Tuple[int, int]]) -> str:
    """Create a concise summary string describing the moderation outcome."""
    # Simple template; in practice you could feed this to an LLM for richer output
    return f"The text {'' if unsafe_spans else 'does not contain'} unsafe content. Detected spans: {unsafe_spans}"
