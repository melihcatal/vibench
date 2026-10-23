# runbook_translate.py
# [LATER-STEP]
# Translate secret‑rotation runbook notes using Anthropic Claude via the anthropic SDK

import os
import json
import anthropic
from typing import Dict, Any


def translate_runbook(runbook_text: str, target_language: str = "es") -> str:
    """Translate a secret‑rotation runbook description to another language using Anthropic Claude.

    Args:
        runbook_text: The original runbook note (English assumed).
        target_language: ISO language code for the desired output (default Spanish).

    Returns:
        The translated text as a string.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Set ANTHROPIC_API_KEY environment variable")

    client = anthropic.Anthropic(api_key=api_key)

    # Prepare Claude request (system prompt ensures translation)
    response = client.completions.create(
        model="claude-3-5-sonnet-20240620",
        temperature=0.0,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Translate the following runbook note into {target_language}:\n\n{runbook_text}",
            }
        ],
        completion_defaults={"stop": ["\n\n"]},
    )
    # The first completion object holds the translated text
    return response.completions[0].text.strip()
