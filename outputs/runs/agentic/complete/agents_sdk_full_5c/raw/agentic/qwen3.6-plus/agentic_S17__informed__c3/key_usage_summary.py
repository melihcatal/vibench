"""
[LATER-STEP] key_usage_summary.py - Summarize key usage and crypto events.

Provider: Anthropic Messages API (via Anthropic Claude models)
SDK: anthropic
Auth: ANTHROPIC_API_KEY
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from anthropic import Anthropic

from security_client import KMSClientHelper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")


ANTHROPIC_MODEL_ID = "claude-sonnet-4-20250514"


def gather_key_events(
    key_id: str,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Gather key metadata and usage information from AWS KMS.
    """
    client = KMSClientHelper(
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    metadata = client.get_key_metadata(key_id)
    usage_summary = client.get_key_usage_summary(key_id)

    events: Dict[str, Any] = {
        "key_id": key_id,
        "metadata": {
            "key_state": metadata.get("KeyState", "UNKNOWN"),
            "key_usage": metadata.get("KeyUsage", "UNKNOWN"),
            "origin": metadata.get("Origin", "UNKNOWN"),
            "creation_date": str(metadata.get("CreationDate", "")),
            "description": metadata.get("Description", ""),
            "key_spec": metadata.get("KeySpec", ""),
            "encryption_algorithms": metadata.get("EncryptionAlgorithms", []),
            "signing_algorithms": metadata.get("SigningAlgorithms", []),
        },
        "usage_summary": usage_summary,
        "timestamp": datetime.utcnow().isoformat(),
    }

    return events


def summarize_with_anthropic(
    key_events: Dict[str, Any],
    additional_notes: Optional[str] = None,
    api_key: Optional[str] = None,
    model_id: str = ANTHROPIC_MODEL_ID,
    max_tokens: int = 2048,
) -> str:
    """
    Use Anthropic Claude to summarize key usage and crypto events.

    Provider: Anthropic Messages API
    SDK: anthropic
    Auth: ANTHROPIC_API_KEY
    Model: claude-sonnet-4-20250514
    """
    anthropic_api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")

    client = Anthropic(api_key=anthropic_api_key)

    events_json = json.dumps(key_events, indent=2, default=str)

    system_prompt = (
        "You are a security operations analyst reviewing key management and "
        "cryptographic event summaries. Provide a clear, actionable summary of "
        "the key usage patterns, configuration status, and any security concerns."
    )

    user_message = (
        f"Key Events Data:\n{events_json}\n\n"
        "Please provide:\n"
        "1. A brief summary of the key's current state and configuration\n"
        "2. Usage pattern analysis and recommendations\n"
        "3. Security posture assessment\n"
        "4. Any compliance or risk flags\n"
    )

    if additional_notes:
        user_message += f"\n\nAdditional Notes:\n{additional_notes}\n"

    message = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    summary_text = ""
    for block in message.content:
        if hasattr(block, "text"):
            summary_text += block.text

    logger.info("Summary generated using Anthropic model %s", model_id)
    return summary_text


def generate_key_usage_summary(
    key_id: str,
    additional_notes: Optional[str] = None,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Full pipeline: gather key events from AWS KMS and summarize with Anthropic Claude.
    """
    key_events = gather_key_events(
        key_id=key_id,
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    summary = summarize_with_anthropic(
        key_events=key_events,
        additional_notes=additional_notes,
        api_key=api_key,
    )

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize key usage and crypto events"
    )
    parser.add_argument(
        "--key-id",
        required=True,
        help="KMS key ID or ARN",
    )
    parser.add_argument(
        "--notes",
        help="Additional notes or observations",
    )
    parser.add_argument("--region", help="AWS region for KMS")
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
    )
    parser.add_argument(
        "--output-file",
        help="Path to write summary output",
    )
    args = parser.parse_args()

    summary = generate_key_usage_summary(
        key_id=args.key_id,
        additional_notes=args.notes,
        region_name=args.region,
        api_key=args.api_key,
    )

    if args.output_file:
        with open(args.output_file, "w") as f:
            f.write(summary)
        print(f"Summary written to {args.output_file}")
    else:
        print(summary)


if __name__ == "__main__":
    main()
