"""
claims_moderation.py - Moderate free-text claims or notes from federated
login profiles using the OpenAI Moderation API.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = "text-moderation-latest"


def moderate_claim_text(
    text: str,
    api_key: str = OPENAI_API_KEY,
    model: str = OPENAI_MODERATION_MODEL,
) -> dict[str, Any]:
    """
    Submit free-text profile claims or notes to OpenAI Moderation API
    to check for policy violations.
    """
    client = OpenAI(api_key=api_key)
    result = client.moderations.create(input=text, model=model)
    mod_result = result.results[0]

    return {
        "flagged": mod_result.flagged,
        "categories": dict(mod_result.categories),
        "category_scores": {
            k: round(v, 6) for k, v in mod_result.category_scores.items()
        },
    }


def moderate_user_notes(
    notes: list[str],
    api_key: str = OPENAI_API_KEY,
    model: str = OPENAI_MODERATION_MODEL,
) -> list[dict[str, Any]]:
    """
    Moderate a list of free-text notes associated with a federated user
    profile using OpenAI's moderation model.
    """
    results = []
    for idx, note in enumerate(notes):
        mod = moderate_claim_text(note, api_key=api_key, model=model)
        results.append({
            "note_index": idx,
            "text_preview": note[:80] + ("..." if len(note) > 80 else ""),
            "flagged": mod["flagged"],
            "categories": mod["categories"],
            "category_scores": mod["category_scores"],
        })
        if mod["flagged"]:
            logger.warning(
                "Federated user note %d flagged by openai moderation: %s",
                idx,
                [k for k, v in mod["categories"].items() if v],
            )
    return results


def batch_moderate_claims(
    claims: dict[str, str],
    api_key: str = OPENAI_API_KEY,
    model: str = OPENAI_MODERATION_MODEL,
) -> dict[str, dict[str, Any]]:
    """
    Batch moderate all string-valued free-text fields in a federated
    user's claim dictionary via OpenAI Moderation API.
    """
    moderated = {}
    for key, value in claims.items():
        if isinstance(value, str) and value.strip():
            mod = moderate_claim_text(value, api_key=api_key, model=model)
            moderated[key] = mod
    return moderated


def is_claim_safe(
    text: str,
    api_key: str = OPENAI_API_KEY,
    model: str = OPENAI_MODERATION_MODEL,
) -> bool:
    """Return True if the claim text passes OpenAI moderation."""
    result = moderate_claim_text(text, api_key=api_key, model=model)
    return not result["flagged"]


if __name__ == "__main__":
    sample_notes = [
        "Standard federated login from Google OAuth.",
        "User requested additional profile verification.",
    ]
    results = moderate_user_notes(sample_notes)
    print(json.dumps(results, indent=2))
