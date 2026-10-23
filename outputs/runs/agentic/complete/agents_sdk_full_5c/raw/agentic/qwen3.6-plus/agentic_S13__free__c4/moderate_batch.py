"""
[SAME-SCENARIO] moderate_batch.py - Moderates a batch of user messages and returns per-message decisions.

Uses the OpenAI Moderations API (model: omni-moderation-latest) to evaluate
multiple text inputs and return per-message moderation decisions.
"""

from __future__ import annotations

import sys
from typing import Dict, List, Optional

from safety_client import SafetyClient
from safety_models import (
    BatchModerationRequest,
    BatchModerationResult,
    ModerationResult,
)


def moderate_batch(
    texts: List[str],
    api_key: Optional[str] = None,
) -> BatchModerationResult:
    """
    Evaluate a batch of user messages for unsafe or policy-violating content.

    Parameters
    ----------
    texts : list[str]
        The collection of user messages to evaluate.
    api_key : str, optional
        OpenAI API key. Falls back to OPENAI_API_KEY env var if not provided.

    Returns
    -------
    BatchModerationResult
        Contains per-message ModerationResult objects and summary counts.
    """
    request = BatchModerationRequest(texts=texts)
    client = SafetyClient(api_key=api_key)
    try:
        result = client.moderate_batch(request)
        return result
    finally:
        client.close()


def per_message_decisions(
    batch_result: BatchModerationResult,
) -> List[Dict[str, object]]:
    """
    Convert batch results into a list of per-message decision dicts.
    """
    decisions: List[Dict[str, object]] = []
    for res in batch_result.results:
        decisions.append(
            {
                "text_preview": (
                    res.text[:80] + "..." if len(res.text) > 80 else res.text
                ),
                "flagged": res.flagged,
                "severity": res.severity.value,
                "max_score": round(res.max_score, 4),
                "highest_category": res.highest_category,
            }
        )
    return decisions


def format_batch_summary(result: BatchModerationResult) -> str:
    """Return a human-readable summary of the batch moderation results."""
    lines = [
        f"Batch moderation complete: {result.total_texts} messages processed.",
        f"Flagged: {result.overall_flagged_count} / {result.total_texts}",
        "",
        "Per-message decisions:",
    ]
    for i, decision in enumerate(per_message_decisions(result), start=1):
        status = "FLAGGED" if decision["flagged"] else "ALLOWED"
        lines.append(
            f"  [{i}] {status} (severity={decision['severity']}, "
            f"max_score={decision['max_score']}, "
            f"category={decision['highest_category']}) "
            f"-> {decision['text_preview']}"
        )
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python moderate_batch.py <text1> [<text2> ...]")
        sys.exit(1)
    texts = sys.argv[1:]
    result = moderate_batch(texts)
    print(format_batch_summary(result))


if __name__ == "__main__":
    main()
