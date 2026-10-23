"""
[SAME-SCENARIO] moderate_text.py - Scores user text for unsafe or policy-violating content.

Uses the OpenAI Moderations API (model: omni-moderation-latest) to evaluate
a single text input and return a structured moderation result.
"""

from __future__ import annotations

import sys
from typing import Optional

from safety_client import SafetyClient
from safety_models import ModerationResult, SeverityLevel


def moderate_text(text: str, api_key: Optional[str] = None) -> ModerationResult:
    """
    Evaluate a single text string for unsafe or policy-violating content.

    Parameters
    ----------
    text : str
        The user-supplied text to evaluate.
    api_key : str, optional
        OpenAI API key. Falls back to OPENAI_API_KEY env var if not provided.

    Returns
    -------
    ModerationResult
        Normalized result including per-category scores and an overall flag.
    """
    if not text or not text.strip():
        return ModerationResult(
            text=text,
            flagged=False,
            severity=SeverityLevel.SAFE,
        )

    client = SafetyClient(api_key=api_key)
    try:
        result = client.moderate_single(text)
        return result
    finally:
        client.close()


def format_decision(result: ModerationResult) -> str:
    """Return a human-readable moderation decision string."""
    status = "FLAGGED" if result.flagged else "ALLOWED"
    lines = [
        f"Status: {status}",
        f"Severity: {result.severity.value}",
        f"Max category score: {result.max_score:.4f}",
    ]
    if result.highest_category:
        lines.append(f"Highest category: {result.highest_category}")
    for cs in result.category_scores:
        lines.append(f"  {cs.category}: {cs.score:.4f} (flagged={cs.flagged})")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python moderate_text.py <text>")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    result = moderate_text(text)
    print(format_decision(result))


if __name__ == "__main__":
    main()
