"""
Summarize key usage and crypto events using Anthropic Claude API.
Anthropic Messages API (anthropic SDK) is the concrete provider for LLM inference.

This module analyzes cryptographic key usage events and generates human-readable
summaries using Anthropic's claude-3-sonnet-20240229 model.
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

import anthropic
from anthropic import Anthropic

from security_models import (
    KeyUsageEvent,
    KeyUsageSummary,
    format_audit_note,
)


# Anthropic Claude model identifier
ANTHROPIC_MODEL = "claude-3-sonnet-20240229"


def summarize_key_usage(
    events: List[KeyUsageEvent],
    key_id: str,
    include_recommendations: bool = True,
) -> str:
    """
    Summarize key usage events using Anthropic Claude API.

    Uses the Anthropic Messages API with claude-3-sonnet-20240229 model
    to analyze cryptographic key usage and generate summaries.

    Args:
        events: List of KeyUsageEvent objects to summarize.
        key_id: The key ID being analyzed.
        include_recommendations: Whether to include security recommendations.

    Returns:
        Human-readable summary string from Anthropic Claude.

    Raises:
        ValueError: If events list is empty.
        anthropic.APIError: If Anthropic API call fails.
    """
    if not events:
        raise ValueError("events list cannot be empty")

    # Build summary statistics
    total = len(events)
    successful = sum(1 for e in events if e.success)
    failed = total - successful

    ops_by_type: Dict[str, int] = {}
    for e in events:
        ops_by_type[e.operation] = ops_by_type.get(e.operation, 0) + 1

    summary = KeyUsageSummary(
        key_id=key_id,
        total_operations=total,
        successful_operations=successful,
        failed_operations=failed,
        operations_by_type=ops_by_type,
        events=events,
    )

    # Build prompt for Anthropic Claude
    events_text = "\n".join(
        f"- [{e.timestamp.isoformat()}] {e.operation}: {'SUCCESS' if e.success else 'FAILED'} - {e.details or 'N/A'}"
        for e in events
    )

    prompt = f"""You are a security analyst reviewing AWS KMS key usage events.

Key ID: {key_id}
Total Operations: {total}
Successful: {successful}
Failed: {failed}
Operations by Type: {json.dumps(ops_by_type)}

Recent Events:
{events_text}

Please provide a concise summary of this key's usage patterns, noting any anomalies or security concerns."""

    if include_recommendations:
        prompt += """

Also provide 2-3 actionable security recommendations based on the usage patterns observed."""

    # Call Anthropic Claude API
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        system="You are an expert security analyst specializing in cryptographic key management and AWS KMS.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    summary_text = message.content[0].text if message.content else ""
    return summary_text


def summarize_crypto_events(
    audit_notes: List[str],
    key_id: str,
) -> str:
    """
    Summarize a list of crypto audit notes using Anthropic Claude.

    Args:
        audit_notes: List of audit note strings.
        key_id: The key ID being analyzed.

    Returns:
        Summary text from Anthropic Claude.
    """
    notes_text = "\n".join(f"- {note}" for note in audit_notes)

    prompt = f"""Review these cryptographic audit notes for key {key_id} and provide a summary:

{notes_text}

Summarize the key security posture and any concerns."""

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=512,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return message.content[0].text if message.content else ""


def main():
    """CLI entry point for key_usage_summary."""
    key_id = os.environ.get("KMS_KEY_ID", "sample-key-id")
    events_json = os.environ.get("KEY_EVENTS", "[]")

    try:
        events_data = json.loads(events_json)
        events = [
            KeyUsageEvent(
                timestamp=datetime.fromisoformat(e.get("timestamp", datetime.now().isoformat())),
                key_id=e.get("key_id", key_id),
                operation=e.get("operation", "Encrypt"),
                success=e.get("success", True),
                details=e.get("details"),
            )
            for e in events_data
        ]
    except Exception as e:
        print(f"Error parsing events: {e}")
        events = [
            KeyUsageEvent(
                timestamp=datetime.now(),
                key_id=key_id,
                operation="Encrypt",
                success=True,
                details="Sample event for testing",
            ),
            KeyUsageEvent(
                timestamp=datetime.now(),
                key_id=key_id,
                operation="Decrypt",
                success=True,
                details="Sample event for testing",
            ),
        ]

    if not events:
        print("No events to summarize")
        exit(1)

    try:
        summary = summarize_key_usage(events, key_id)
        print("Key Usage Summary:")
        print(summary)
    except Exception as e:
        print(f"Summary generation failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
