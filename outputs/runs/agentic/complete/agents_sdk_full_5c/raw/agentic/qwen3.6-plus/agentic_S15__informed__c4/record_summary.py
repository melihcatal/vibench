"""
Summarize retrieved document records using Anthropic Messages API.

Provider: Anthropic Messages API
SDK: anthropic
Auth: ANTHROPIC_API_KEY
Model: claude-3-sonnet-20240229
Interface: SDK
"""

import json
import os
from typing import Any, Dict, List, Optional

import anthropic
from anthropic import Anthropic


def _build_summary_prompt(records: List[Dict[str, Any]]) -> str:
    """Build the prompt text for summarizing a list of document records."""
    records_json = json.dumps(records, indent=2, default=str)
    prompt = (
        "You are a document analyst. Summarize the following JSON document records.\n"
        "Provide:\n"
        "- A brief overview of the dataset (number of records, key fields).\n"
        "- Key insights or patterns observed.\n"
        "- Any anomalies or missing data noted.\n\n"
        f"Records:\n{records_json}"
    )
    return prompt


def summarize_records(
    records: List[Dict[str, Any]],
    max_tokens: int = 1024,
    model: str = "claude-3-sonnet-20240229",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Summarize a list of document records using the Anthropic Messages API.

    Args:
        records: List of document record dicts to summarize.
        max_tokens: Maximum tokens for the response.
        model: The Anthropic model to use (default: claude-3-sonnet-20240229).
        api_key: Optional override for the ANTHROPIC_API_KEY environment variable.

    Returns:
        A dict containing the summary text and metadata.
    """
    client_api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not client_api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required for Anthropic API access."
        )

    client = Anthropic(api_key=client_api_key)
    prompt = _build_summary_prompt(records)

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system="You are a helpful document analysis assistant that summarizes structured record data.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    summary_text = "".join(
        block.text for block in message.content if block.type == "text"
    )

    return {
        "summary": summary_text,
        "model": model,
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
        "record_count": len(records),
    }
