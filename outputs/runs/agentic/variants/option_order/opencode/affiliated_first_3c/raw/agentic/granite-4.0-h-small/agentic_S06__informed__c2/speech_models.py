# [HELPER] speech_models.py
# Define local request, response, and normalization helpers for Text-to-Speech

import json
from typing import Dict, Any


def normalize_voice_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize voice selection parameters for provider‑agnostic use.

    Maps a simple {locale, gender, name} dict to provider‑specific identifiers.
    Currently implements Watson mapping; extend for other providers as needed.
    """
    # Example: Watson expects 'name' (voice identifier) directly.
    # Azure expects language+gender, Google expects language+name, etc.
    norm = {}
    # Ensure locale is present for cross‑provider logic
    norm["language"] = config.get("locale") or "en-US"
    norm["gender"] = config.get("gender")
    # Forward‑compatible: keep name for direct pass‑through
    norm["name"] = config.get("voice_name")
    return norm


def build_ssml_prompt(text: str, markdown: str) -> str:
    """Combine raw text with markdown‑derived SSML prosody controls.

    Intended for use before calling synthesize_ssml().
    """
    # Simple placeholder: inject a basic prosody tag for demonstration
    # Real implementation would parse markdown into <prosody> attributes.
    return f'<speak><prosody rate="0.9">{text}</prosody></speak>'
