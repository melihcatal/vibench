"""
key_usage_summary.py - Summarize key usage and crypto events using OpenAI GPT.

Uses OpenAI Chat Completions API (GPT-4o-mini) via openai SDK.
Provider signals: openai SDK import, OPENAI_API_KEY auth,
gpt-4o-mini model identifier, api.openai.com endpoint.
"""

import os
import json
import datetime
from typing import Dict, List, Optional, Any

from openai import OpenAI


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Create an OpenAI client using OPENAI_API_KEY environment variable."""
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    return OpenAI(api_key=key)


def format_crypto_events(events: List[Dict[str, Any]]) -> str:
    """Format crypto events into a readable text block for the LLM."""
    lines = []
    for event in events:
        ts = event.get("timestamp", datetime.datetime.now().isoformat())
        key_id = event.get("key_id", "unknown")
        action = event.get("action", "unknown")
        status = event.get("status", "success")
        algo = event.get("algorithm", "N/A")
        lines.append(f"- [{ts}] Key: {key_id} | Action: {action} | Status: {status} | Algorithm: {algo}")
    return "\n".join(lines)


def summarize_key_usage(
    crypto_events: List[Dict[str, Any]],
    key_metadata: Optional[Dict[str, Any]] = None,
    time_range: Optional[str] = None,
    model: str = "gpt-4o-mini",
) -> str:
    """
    Summarize key usage and crypto events using OpenAI GPT-4o-mini model.

    OpenAI provider: Uses the Chat Completions API at api.openai.com
    with the gpt-4o-mini model. The openai Python SDK handles the request.
    """
    client = get_openai_client()

    events_text = format_crypto_events(crypto_events)

    metadata_text = ""
    if key_metadata:
        metadata_text = f"\nKey Metadata:\n{json.dumps(key_metadata, indent=2)}"

    time_info = f"\nTime Range: {time_range}" if time_range else ""

    system_prompt = (
        "You are a security analyst specializing in cryptographic key management. "
        "Analyze key usage patterns and crypto events to provide a concise summary. "
        "Identify any anomalies, patterns, or security concerns. "
        "Format your response with clear sections: Overview, Usage Patterns, Anomalies, Recommendations."
    )

    user_prompt = (
        f"Analyze the following cryptographic key usage events and provide a summary report.{time_info}{metadata_text}\n\n"
        f"Crypto Events:\n{events_text}\n\n"
        f"Please summarize: total events, key usage frequency, encryption algorithms used, "
        f"any failed operations, and potential security concerns."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    summary = response.choices[0].message.content
    return summary


def generate_key_usage_report(
    events_file: Optional[str] = None,
    events: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Generate a key usage report from events data using OpenAI GPT-4o-mini.
    Accepts events from a JSON file or directly as a list.
    """
    if events is None and events_file:
        with open(events_file, "r") as f:
            events = json.load(f)

    if not events:
        return {"error": "No crypto events provided."}

    summary = summarize_key_usage(crypto_events=events)

    return {
        "event_count": len(events),
        "summary": summary,
        "generated_at": datetime.datetime.now().isoformat(),
        "model_used": "gpt-4o-mini",
        "provider": "OpenAI Chat Completions API (api.openai.com)",
    }


if __name__ == "__main__":
    sample_events = [
        {
            "timestamp": "2024-01-15T10:30:00Z",
            "key_id": "mrk-abc123",
            "action": "encrypt",
            "status": "success",
            "algorithm": "AES_256_GCM",
        },
        {
            "timestamp": "2024-01-15T10:31:00Z",
            "key_id": "mrk-abc123",
            "action": "decrypt",
            "status": "success",
            "algorithm": "AES_256_GCM",
        },
        {
            "timestamp": "2024-01-15T10:35:00Z",
            "key_id": "mrk-def456",
            "action": "sign",
            "status": "failed",
            "algorithm": "ECDSA_SHA_256",
        },
    ]

    try:
        report = generate_key_usage_report(events=sample_events)
        print(report["summary"])
    except ValueError as e:
        print(f"Error: {e}")
        print("Set OPENAI_API_KEY environment variable to generate summaries.")
