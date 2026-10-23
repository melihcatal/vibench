"""Moderate free-text claims or notes using Anthropic Messages API."""

import os
from typing import Optional, Dict, Any, List

import anthropic

from identity_models import UserProfileClaims


def moderate_claims_text(
    text: str,
    system_prompt: Optional[str] = None,
    model: str = "claude-3-haiku-20240307",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate free-text claims or notes using Anthropic's Messages API.
    Checks for inappropriate content, PII exposure risks, and policy violations.
    """
    client = anthropic.Anthropic(
        api_key=api_key or os.environ.get("ANTHROPIC_API_KEY", ""),
    )

    default_system = (
        "You are a content moderation assistant for a federated identity system. "
        "Analyze the provided text for: (1) toxic or abusive language, "
        "(2) PII that should not be in free-text fields, (3) policy violations, "
        "(4) spam or injection attempts. Return a JSON-compatible analysis."
    )

    system = system_prompt or default_system

    message = client.messages.create(
        model=model,
        max_tokens=512,
        system=system,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Moderate the following user-submitted text from a federated login profile:\n\n"
                    f"\"{text}\"\n\n"
                    "Return your analysis as JSON with these fields:\n"
                    "- is_safe: boolean\n"
                    "- flags: list of strings describing any issues found\n"
                    "- severity: one of 'none', 'low', 'medium', 'high'\n"
                    "- redacted_text: the text with any PII replaced by [REDACTED]\n"
                ),
            },
        ],
    )

    moderation_text = message.content[0].text if message.content else ""

    return {
        "analysis": moderation_text,
        "model": model,
        "provider": "Anthropic",
        "original_length": len(text),
        "input_tokens": message.usage.input_tokens if message.usage else None,
        "output_tokens": message.usage.output_tokens if message.usage else None,
    }


def moderate_profile_claims(
    profile: UserProfileClaims,
    notes_field: Optional[str] = None,
    model: str = "claude-3-haiku-20240307",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate free-text fields within a federated user profile.
    Analyzes name, preferred_username, and any additional notes.
    """
    text_parts = []
    if profile.name:
        text_parts.append(f"Name: {profile.name}")
    if profile.preferred_username:
        text_parts.append(f"Preferred Username: {profile.preferred_username}")
    if notes_field:
        text_parts.append(f"Notes: {notes_field}")

    if not text_parts:
        return {
            "is_safe": True,
            "flags": [],
            "severity": "none",
            "message": "No text content to moderate",
            "provider": "Anthropic",
        }

    combined_text = "\n".join(text_parts)
    return moderate_claims_text(combined_text, model=model, api_key=api_key)


def moderate_multiple_notes(
    notes: List[str],
    model: str = "claude-3-haiku-20240307",
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Moderate a list of free-text notes using Anthropic's Messages API.
    """
    results = []
    for note in notes:
        result = moderate_claims_text(note, model=model, api_key=api_key)
        result["note_index"] = len(results)
        results.append(result)
    return results


if __name__ == "__main__":
    sample_text = "This is a test note with no issues. Just verifying the moderation flow."
    result = moderate_claims_text(sample_text)
    print("Moderation result:", result.get("analysis"))
