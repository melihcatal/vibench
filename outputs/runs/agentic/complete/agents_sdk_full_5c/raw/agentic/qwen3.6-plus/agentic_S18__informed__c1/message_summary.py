"""
[LATER-STEP] Summarize message processing results using Anthropic Messages API.
Provider: Anthropic
SDK: anthropic
Auth: ANTHROPIC_API_KEY
Model: claude-3-haiku-20240307
"""

import os
import json
from typing import List, Dict, Any, Optional
from messaging_models import ConsumeResult


def summarize_message_processing(
    results: List[Dict[str, Any]],
    model: str = "claude-3-haiku-20240307",
    api_key: str = None,
) -> str:
    """
    Use Anthropic Claude to generate a summary of message processing results.

    Args:
        results: List of processing result dicts with keys like
                 'event_type', 'status', 'message_id', 'source'.
        model: Anthropic model identifier (default: claude-3-haiku-20240307).
        api_key: Anthropic API key.

    Returns:
        A natural-language summary of the processing results.
    """
    import anthropic

    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = (
        "You are a messaging system analyst. Summarize the message processing "
        "results provided. Include counts by event type, success/failure rates, "
        "and any notable patterns or anomalies."
    )

    user_prompt = (
        f"Here are the message processing results:\n\n{json.dumps(results, indent=2)}\n\n"
        "Please provide a concise summary of these results."
    )

    response = client.messages.create(
        model=model,
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    summary_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            summary_text += block.text

    return summary_text


def summarize_consume_results(
    consume_results: List[ConsumeResult],
    model: str = "claude-3-haiku-20240307",
    api_key: str = None,
) -> str:
    """
    Summarize a list of ConsumeResult objects using Anthropic Claude.

    Args:
        consume_results: List of ConsumeResult from consume operations.
        model: Anthropic model identifier.

    Returns:
        A natural-language summary.
    """
    results_data = []
    for cr in consume_results:
        entry: Dict[str, Any] = {
            "message_id": cr.message_id,
            "acknowledged": cr.acknowledged,
            "delivery_attempt": cr.delivery_attempt,
        }
        if cr.event:
            entry["event_type"] = cr.event.event_type
            entry["source"] = cr.event.source
            entry["event_id"] = cr.event.event_id
        results_data.append(entry)

    return summarize_message_processing(results_data, model=model, api_key=api_key)
